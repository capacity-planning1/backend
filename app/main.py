from fastapi import FastAPI


app = FastAPI(
    title='Capacity Planning API',
    version='1.0.0',
)


@app.get('/')
def read_root():
    return {'message': 'Capacity Planning API is running'}
