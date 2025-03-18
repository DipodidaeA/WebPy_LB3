from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from Db.SQLAlchemy.Func import get_all_days, add_day, update_day, delete_day
from DTO.DTO import DTO
from Db.PostgreSQL.Fucn import get_all_days_pg, add_day_pg, update_day_pg, delete_day_pg
from Db.DbMigrates import mgrate_SQLite_on_PG, mgrate_PG_on_SQLite
from Routes.FileMenege import save, load

router = APIRouter()

# отримуємо сторінку користувача
@router.get("/")
def root():
    return FileResponse("Html/User.html", media_type="text/html")

# перейти з адміна на користувача
# переадресація на сторінку користувача
@router.get("/user")
def user():
    return RedirectResponse("/", status_code=302)

# авторизація адміна, коли правильно
# переадресація на сторінку адміна
@router.get("/authorization/{passw}")
def authorization(passw: int):
    if passw != 123:
        return JSONResponse(status_code=403, content={"detail": "Payment Required"})
    
    return RedirectResponse("/admin", status_code=302)

# отримуємо сторінку адміна
@router.get("/admin")
def admin():
    return FileResponse("Html/Admin.html", media_type="text/html")

# отримати список днів
@router.get("/days")
def read_days():
    # отримуємо позначку БД з файл DbState.txt
    active_DB = load()

    # для SQLite
    if active_DB == "alch":
        days = get_all_days()
    # для PostgreSQL
    if active_DB == "pg":
        days = get_all_days_pg()

    return days

# щоб змінити БД SQLite на PostgreSQL
@router.get("/admin/use/pg")
def use_pg():
    # отримуємо позначку БД з файл DbState.txt
    active_DB = load()

    if active_DB == "pg":
        return JSONResponse(status_code=200, content={"Message": "DB already PG"})
    
    # міграцію даних
    mgrate_SQLite_on_PG()
    # зберігаємо позначку БД у файл DbState.txt
    save("pg")

    return JSONResponse(status_code=200, content={"Message": "DB chenged"})

# щоб змінити БД PostgreSQL на SQLite
@router.get("/admin/use/alch")
def use_alch():
    active_DB = load()

    if active_DB == "alch":
        return JSONResponse(status_code=200, content={"Message": "DB already ASQAlchemy"})
    
    mgrate_PG_on_SQLite()

    save("alch")

    return JSONResponse(status_code=200, content={"Message": "DB chenged"})

# додавання дня
@router.post("/admin/day")
def create_day(dto: DTO):
    active_DB = load()

    if active_DB == "alch":
        day = add_day(dto)
    if active_DB == "pg":
        day = add_day_pg(dto)

    return day

# оновлення дня
@router.put("/admin/day")
def chenge_day(dto: DTO):
    active_DB = load()

    if active_DB == "alch":
        day = update_day(dto)
    if active_DB == "pg":
        day = update_day_pg(dto)

    if day == None:
        return JSONResponse(status_code=404, content={"Day not found"})
    
    return day

# видалення дня
@router.delete("/admin/day/{id}")
def remove_day(id: int):
    active_DB = load()

    if active_DB == "alch":
        day = delete_day(id)
    if active_DB == "pg":
        day = delete_day_pg(id)

    if day == None:
        return JSONResponse(status_code=404, content={"Day not found"})
    
    return day