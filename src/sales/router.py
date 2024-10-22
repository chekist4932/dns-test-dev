from fastapi import APIRouter

router = APIRouter(prefix='/api', tags=['sales'])


@router.get('/sales')
async def get_sales():
    return {'message': 'Hello world!'}
