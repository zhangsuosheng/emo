from elasticsearch import Elasticsearch
from django.conf import settings

class Elastic_opter():
    def __init__(self,host,port):
        self.els_conn=Elasticsearch(host,port=port)

    # 为每个用户创建一个index
    def create_user_index(self,username):
        if self.els_conn.indices.exists(index=username) is not True:
            result=self.els_conn.indices.create(index=username)
            if result['acknowledged']==True:
                return 0#'index created successfully'
            else:
                return 1#'用户名只接受小写字母'
        else:
            return 2#'该用户名可能已注册，如有疑问联系管理员'

    # 为用户的每个好友创建一个document
    def insert_friend_docu(self,username,docu_list):
        #elem in docu_list: {'attr1':'value1','attr2':'value2'}
        if self.els_conn.indices.exists(index=username) is True:
            for elem in docu_list:
                self.els_conn.index(index=username,doc_type=settings.FRIENDS_TYPE_NAME,body=elem)
        else:
            return False#index不存在

    # 批量修改某个用户的多个好友信息
    def modify_docu(self,username,docu_list):
        if self.els_conn.indices.exists(index=username) is True:
            for elem in docu_list:
                query_dict = {
                    'query': {
                        'match': {
                            settings.FRIEND_ID_NAME: username
                        }
                    }
                }
                result = self.els_conn.search(index=username, doc_type=settings.FRIENDS_TYPE_NAME, body=query_dict)
                print("############################")
                print(result)
        else:
            return False#index不存在

    def query_friend_docu(self,username,query_dict):
        result=self.els_conn.search(index=username,doc_type=settings.FRIENDS_TYPE_NAME,body=query_dict)
        print(result)
        print("$$$$$$$$$$$$$$$$$$$$$$")
        # 查询得到的result直接就是dict类型
        return result