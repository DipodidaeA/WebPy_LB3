from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from Db.SQLAlchemy.Func import get_all_days, add_day, update_day, delete_day
from DTO.DTO import DTO
from Db.MongoDB.Func import get_all_days_mo, add_day_mo, update_day_mo, delete_day_mo
from Routes.FileMenege import save, load
from Db.DbMigrates import mgrate_MO_on_SQLite, mgrate_SQLite_on_MO

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
    # для MongoDB
    if active_DB == "mo":
        days = get_all_days_mo()

    return days

# щоб змінити БД SQLite на PostgreSQL
@router.get("/admin/use/mo")
def use_mo():
    # отримуємо позначку БД з файл DbState.txt
    active_DB = load()

    if active_DB == "mo":
        return JSONResponse(status_code=200, content={"Message": "DB already MO"})
    
    # міграцію даних
    mgrate_SQLite_on_MO()
    # зберігаємо позначку БД у файл DbState.txt
    save("mo")

    return JSONResponse(status_code=200, content={"Message": "DB chenged"})

# щоб змінити БД PostgreSQL на SQLite
@router.get("/admin/use/alch")
def use_alch():
    active_DB = load()

    if active_DB == "alch":
        return JSONResponse(status_code=200, content={"Message": "DB already ASQAlchemy"})
    
    mgrate_MO_on_SQLite()

    save("alch")

    return JSONResponse(status_code=200, content={"Message": "DB chenged"})

# додавання дня
@router.post("/admin/day")
def create_day(dto: DTO):
    active_DB = load()

    if active_DB == "alch":
        day = add_day(dto)
    if active_DB == "mo":
        day = add_day_mo(dto)

    return day

# оновлення дня
@router.put("/admin/day")
def chenge_day(dto: DTO):
    active_DB = load()

    if active_DB == "alch":
        day = update_day(dto)
    if active_DB == "mo":
        day = update_day_mo(dto)

    if day == None:
        return JSONResponse(status_code=404, content={"Day not found"})
    
    return day

# видалення дня
@router.delete("/admin/day/{id}")
def remove_day(id: str):
    active_DB = load()

    if active_DB == "alch":
        day = delete_day(int(id))
    if active_DB == "mo":
        day = delete_day_mo(id)

    if day == None:
        return JSONResponse(status_code=404, content={"Day not found"})
    
    return day