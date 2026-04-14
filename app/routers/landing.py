from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi import Request, status
from app.dependencies.auth import IsUserLoggedIn, get_current_user 
from app.dependencies.session import SessionDep
from . import router, templates 

@router.get("/", response_class=HTMLResponse) 
async def landing_view(
    request: Request, 
    user_logged_in: IsUserLoggedIn, 
    db: SessionDep
): 
    
    if user_logged_in:
        user = await get_current_user(request, db) 
        return RedirectResponse(url=request.url_for('user_home_view'), status_code=status.HTTP_303_SEE_OTHER) 
    
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
    ) 
