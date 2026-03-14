from fastapi import FastAPI, Query, HTTPException
from schema import (AdvCreateRequest, AdvCreateResponse, AdvGetResponse,
                    AdvDeleteResponse, AdvUpdateRequest, AdvSearchResponse,
                    AdvUpdateResponse, CreateUserRequest,
                    CreateUserResponse, LoginRequest, LoginResponse, UserGetResponse,
                    UserUpdateResponse, UserUpdateRequest, UserDeleteResponse
                    )
from lifespan import lifespan
from dependency import SessionDependency, TokenDependency
from constants import SUCCESS_RESPONSE
from sqlalchemy import select, func
from authentication import hash_password, check_password
import models
import crud


app = FastAPI(
    title='Advertisement API ',
    description='Реализация API сервиса объявлений',
    lifespan=lifespan,
    )


@app.get('/api/advertisement/{adv_id}',
         tags=["Advertisement"], response_model=AdvGetResponse)
async def get_advertisement(adv_id: int, session: SessionDependency):
    """
    Асинхронная функция получения объявления из БД по id
    :param adv_id: id объявления
    :param session: объект сессии БД
    :return: словарь с параметрами объявления
    """
    adv_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    return adv_obj.dict

@app.post('/api/advertisement',
          tags=["Advertisement"], response_model=AdvCreateResponse)
async def create_advertisement(adv: AdvCreateRequest,
                               session: SessionDependency,
                               token: TokenDependency):
    """
    Асинхронная функция создания объявления
    :param adv: параметры объявления по шаблону
    :param session: объект сессии БД
    :param token: токен, передаваемый пользователем
    :return: возвращаем словарь с id созданного объявления
    """
    adv_dict = adv.model_dump(exclude_unset=True)
    adv_obj = models.Adv(**adv_dict, user_id = token.user_id)
    await crud.add_item(session, adv_obj)
    return adv_obj.id_dict

@app.patch('/api/advertisement/{adv_id}', tags=["Advertisement"],
           response_model=AdvUpdateResponse)
async def patch_advertisement(adv_id: int,
                              adv_data: AdvUpdateRequest,
                              session: SessionDependency,
                              token: TokenDependency):
    """
    Асинхронная функция изменения существующего объявления
    :param adv_id: id объявления
    :param adv_data: новые параметры объявления по шаблону
    :param session: объект сессии БД
    :param token: токен, передаваемый пользователем
    :return: возвращается результат работы функции(успех, не успех)
    """
    adv_dict = adv_data.model_dump(exclude_unset=True)
    adv_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    if token.user.role == "admin" or token.user.id == adv_obj.user_id:
        for field, value in adv_dict.items():
            setattr(adv_obj, field, value)
        await crud.add_item(session, adv_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=403, detail="Insufficient privileges")

@app.delete('/api/advertisement/{adv_id}', tags=["Advertisement"],
            response_model=AdvDeleteResponse)
async def delete_advertisement(adv_id: int,
                               session: SessionDependency,
                               token: TokenDependency):
    """
    Асинхронная функция удаления объявления
    :param adv_id: id объявления
    :param session: объект сессии БД
    :param token: токен, передаваемый пользователем
    :return: возвращается результат работы функции(успех, не успех)
    """
    adv_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    if token.user.role == "admin" or token.user.id == adv_obj.user_id:
        await crud.delete_item(session, adv_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=403, detail="Insufficient privileges")

@app.get('/api/advertisement', tags=["Advertisement"],
         response_model=AdvSearchResponse)
async def search_advertisement(session: SessionDependency,
                               query_string: str = Query(...)):
    """
    Асинхронная функция полнотекстового поиска объявлений
    по полям title и description.
    :param query_string: поисковый запрос
    :param session: объект сессии БД
    :return: возвращается список найденных объявлений
    """
    # Преобразуем строку поиска в ts_query объект
    query_vector = func.to_tsvector(
        func.concat(models.Adv.title, ' ', models.Adv.description)
    )
    query_match = func.plainto_tsquery(query_string)

    # Создаем запрос с использованием полнотекстового поиска
    query = (
        select(models.Adv)
        # Операция сравнения вектора с искомым текстом
        .where(query_vector.op("@@")(query_match))
    )
    # Выполняем запрос и возвращаем найденные объявления
    result = await session.execute(query)
    adv_objects = result.unique().scalars().all()  # Получаем список объектов
    return {"results": [adv.dict for adv in adv_objects]}


@app.post('/api/user', tags=["user"], response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest,
                      session: SessionDependency):
    """
    Функция создания нового пользователя

    :param user_data: данные создаваемого пользователя по шаблону
    :param session: объект сессии БД
    :return: возврат id созданного пользователя
    """
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_orm_obj = models.User(**user_dict)
    await crud.add_item(session, user_orm_obj)
    return user_orm_obj.id_dict


@app.post("/api/login", tags=["login"], response_model=LoginResponse)
async def login(login_data: LoginRequest, session: SessionDependency):
    """
    Асинхронная функция "логина" пользователя,
    если пароль верен, создается токен
    для дальнейшего использования в API

    :param login_data: данные пользователя по шаблону
    :param session: объект сессии БД
    :return: токен для пользователя
    """
    query = select(models.User).where(models.User.name == login_data.name)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(401, "Invalid credentials")
    if not check_password(login_data.password, user.password):
        raise HTTPException(401, "Invalid credentials")
    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict

@app.get('/api/user/{user_id}', tags=["user"], response_model=UserGetResponse)
async def get_user(user_id: int, session: SessionDependency):
    """
    Асинхронная функция получения пользователя из БД по id
    :param user_id: id пользователя
    :param session: объект сессии БД
    :return: словарь с параметрами пользователя по шаблону
    """
    user_obj = await crud.get_item_by_id(session, models.User, user_id)
    return user_obj.dict

@app.patch('/api/user/{user_id}', tags=["user"],
           response_model=UserUpdateResponse)
async def patch_user(user_id: int, user_data: UserUpdateRequest,
                     session: SessionDependency, token: TokenDependency):
    """
    Асинхронная функция изменения параметров пользователя в БД
    :param user_id: id пользователя
    :param user_data: изменяемы данные по шаблону
    :param session: объект сессии БД
    :param token: токен пользователя
    :return: результат работы функции (успешно/не успешно)
    """
    user_dict = user_data.model_dump(exclude_unset=True)
    user_obj = await crud.get_item_by_id(session, models.User, user_id)
    if token.user.role == "admin" or token.user.id == user_obj.user_id:
        if "password" in user_dict:
            user_dict["password"] = hash_password(user_dict["password"])
        for field, value in user_dict.items():
            setattr(user_obj, field, value)
        await session.commit()
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=403, detail="Insufficient privileges")

@app.delete('/api/user/{user_id}', tags=["user"],
            response_model=UserDeleteResponse)
async def delete_user(user_id: int, session: SessionDependency,
                      token: TokenDependency):
    """
    Асинхронная функция удаления пользователя из БД
    :param user_id: id пользователя
    :param session: объект сессии БД
    :param token: токен пользователя
    :return: результат работы функции (успешно/не успешно)
    """
    user_obj = await crud.get_item_by_id(session, models.User, user_id)
    if token.user.role == "admin" or token.user.id == user_obj.id:
        await crud.delete_item(session, user_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=403, detail="Insufficient privileges")