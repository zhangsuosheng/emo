from elasticsearch import Elasticsearch
from django.conf import settings

class Elastic_opter():
    def __init__(self,host,port):
        self.els_conn=Elasticsearch(host,port=port)

    def create_user_index(self,username):
        if self.els_conn.indices.exists(index=username) is not True:
            result=self.els_conn.indices.create(index=username)
            if result['acknowledged']==True:
                return 0#'index created successfully'
            else:
                return 1#'用户名只接受小写字母'
        else:
            return 2#'该用户名可能已注册，如有疑问联系管理员'

    def insert_friend_docu(self,username,docu_list):
        #elem in docu_list: {'attr1':'value1','attr2':'value2'}
        if self.els_conn.indices.exists(index=username) is True:
            for elem in docu_list:
                self.els_conn.index(index=username,doc_type=settings.FRIENDS_TYPE_NAME,body=elem)
        else:
            return False#index不存在

    def modify_docu(self,username,docu_list):
        if self.els_conn.indices.exists(index=username) is True:
            for elem in docu_list:
                query_sentence = {
                    'query': {
                        'match': {
                            settings.FRIEND_ID_NAME: username
                        }
                    }
                }
                result = self.els_conn.search(index=username, doc_type=settings.FRIENDS_TYPE_NAME, body=query_sentence)
                print("############################")
                print(result)
        else:
            return False#index不存在
