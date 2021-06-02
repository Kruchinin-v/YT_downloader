def get_config():
    import os
    import yaml
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # path_to_conf = os.path.join(BASE_DIR, 'backend', 'environments', 'conf.json')
    path_to_conf = os.path.join(BASE_DIR, 'conf.yml')

    answer = {
        'status': 'OK',
        'result': '',
        'detail': '',
    }

    with open(path_to_conf, 'r') as stream:
        try:
            answer['result'] = yaml.load(stream, Loader=yaml.FullLoader)
            answer['result']['BASE_DIR'] = BASE_DIR
        except Exception as e:
            answer['result'] = "Ошибка чтение конфигурации"
            answer['detail'] = e

    return answer
