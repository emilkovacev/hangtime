from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

async def login(request):
    return templates.TemplateResponse('login.html', {'request': request})
