# from django.test import TestCase  
# from leaderboard.models import Entry  
# from model.models import Model,ModelVersion
# from dataset.models import Dataset
# from core.models import Language,Modality
# class EntryTestCase(TestCase):  
#     def setUp(self):
#         self.model_instance = ModelVersion.objects.create(name='test')
#         self.language_instance = Language.objects.create(name='hindi')
#         self.modality_instance = Modality.objects.create(name='printed')
#         self.dataset_instance = Dataset.objects.create(
#             name='test',
#             language=self.language_instance,
#             modality=self.modality_instance,
#             file='/home/krishna/bhashini_website/media/Datasets/book_14.json'
#         ) 

#     def test_model_name(self):  
#         self.assertEqual(self.model_instance.name, 'test')  