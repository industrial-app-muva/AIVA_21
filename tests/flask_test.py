import io
import unittest

import cv2
from PIL import Image
from bs4 import BeautifulSoup

from app import app, allowed_file


class TestApp(unittest.TestCase):

    @staticmethod
    def get_image_bytes(img):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        raw_bytes = io.BytesIO()
        img.save(raw_bytes, "JPEG")
        raw_bytes.seek(0)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

        return raw_bytes

    def setUp(self) -> None:
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        self.app = app
        self.client = self.app.test_client()
        self.image_name = "rec1-3.jpg"
        self.image_path = './static/image/rec1-3.jpg'
        self.img = Image.fromarray(cv2.imread(self.image_path, 1))

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_health_check(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        res = self.client.get('/health-check')
        self.assertEqual(200, res.status_code, 'Wrong response')
        self.assertEqual(b'Online', res.data, 'Wrong check message')

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_init_gui(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        res = self.client.get('/')
        self.assertEqual(200, res.status_code, 'Wrong response')
        self.assertIn(b'CD', res.data, 'Wrong Jinja2 template')

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_process_img_empty_data(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        res = self.client.post('/process_img',
                               content_type='multipart/form-data',
                               data={})
        self.assertEqual(400, res.status_code)
        self.assertTrue(res.json['error'] == 400 and res.json['text'] == 'Bad request')

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_process_img_good_case(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        raw_bytes = self.get_image_bytes(self.img)
        data_correct = dict(file=(raw_bytes, self.image_name))

        res = self.client.post('/process_img',
                               content_type='multipart/form-data',
                               data=data_correct)
        raw_bytes.close()

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json['bboxs'] is not None)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_process_img_empty_filename(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        raw_bytes = self.get_image_bytes(self.img)
        data_empty_filename = dict(file=(raw_bytes, ""))

        res = self.client.post('/process_img',
                               content_type='multipart/form-data',
                               data=data_empty_filename)
        raw_bytes.close()

        self.assertEqual(400, res.status_code)
        self.assertTrue(res.json['error'] == 400 and res.json['text'] == 'Bad request')

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_process_img_gui_good_case(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        raw_bytes = self.get_image_bytes(self.img)
        data_correct = dict(file=(raw_bytes, self.image_name))

        res = self.client.post('/process_img_gui',
                               content_type='multipart/form-data',
                               data=data_correct)
        raw_bytes.close()

        self.assertEqual(200, res.status_code, 'Wrong response')

        soup = BeautifulSoup(res.data, 'html.parser')
        images = soup.findAll('img')

        self.assertEqual(2, len(images))

        for img in images:
            src = img.attrs['src']
            self.assertTrue(src != "" or src is not None)
            self.assertIn('data:image/jpeg;base64', src)

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_process_img_gui_empty_filename(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        raw_bytes = self.get_image_bytes(self.img)
        data_empty_filename = dict(file=(raw_bytes, ""))

        res = self.client.post('/process_img_gui',
                               content_type='multipart/form-data',
                               data=data_empty_filename)
        raw_bytes.close()

        self.assertEqual(200, res.status_code, 'Wrong response')
        self.assertIn(b'CD', res.data, 'Wrong Jinja2 template')

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')

    def test_allowed_file(self):
        print(f'Executing {sys._getframe(  ).f_code.co_name}...')

        bad_filename = 'bad_filename.err'
        self.assertFalse(allowed_file(bad_filename))

        good_filename_lower = 'good_filename.png'
        good_filename_upper = 'good_filename.PNG'

        self.assertTrue(
            allowed_file(good_filename_lower)
            and
            allowed_file(good_filename_upper)
        )

        print(f'Completed {sys._getframe(  ).f_code.co_name}!')
