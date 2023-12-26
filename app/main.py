from fastapi import FastAPI, Depends

from .routers import items, users
from . import dependencies

# *** Note on relative importing ***
# The number of dots you is the number of directories it takes for you to get to the target following the dot
# You count the number of dots up from the file that you're currently in


app = FastAPI(dependencies=[Depends(dependencies.verify_access_token)])  # declare a global dependency for all routes

bar: set = set()

app.include_router(users.router)    # use the include_router to add routers to your FastAPI instance
app.include_router(
    items.router,
    prefix='/items',    # you can specify the params of the router inside the include_router function instead of inside
    tags=['items']      # the APIRouter definition itself so that you preserve the sovereignty of the router
                        # for example if you're sharing it across your app, and you want to remove tight coupling
    # So, for example, other projects could use the same APIRouter with a different dependency or authentication method.

    # 'prefix' is the url prefix of this router that will group together its path operations
    # 'tags' is used to group the path operations together in the OpenAPI docs instead of just listing them contiguously
    #       'tags' is an array of strings
)


@app.get('/', tags=['home'])
def home():
    return "Welcome Home Bud!"


# to use uvicorn to run a nested FastAPI instance, you'll use dots to reference it
# e.g uvicorn app.main:app --reload (we used dot notation to access the nested file main.py
