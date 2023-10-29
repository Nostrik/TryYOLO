import pytest

from core import start_predict


def test_start_predict_func(capsys):
    result = start_predict(
        weigth_file='C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input\\syringe.pt',
        target_video='C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input\\5.mp4',
        object_name='test_run',
    )
    captured = capsys.readouterr()
    print(captured)
