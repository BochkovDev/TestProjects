from fastapi.templating import Jinja2Templates

from .settings import settings


templates = Jinja2Templates(directory=settings.TEMPLATES.TEMPLATE_DIR)