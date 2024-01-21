from parsing_stores.auto_parsing.selery_app import app
from parsing_stores.lenta.main import main


@app.task
def run_src_lenta():
    print('ТАСКА ТАСКА ТАСКА ТАСКА')
    main()
