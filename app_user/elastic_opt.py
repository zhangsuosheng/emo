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


    # 批量插入docu到message type中
    def insert_message_docu(self,username,docu_list,id_list,doc_type=settings.MESSAGE_TYPE_NAME):
        if self.els_conn.indices.exists(index=username) is True:
            for i in range(0,len(docu_list)):
                self.els_conn.index(index=username,doc_type=doc_type,body=docu_list[i],id=id_list[i])
        else:
            return False  # index不存在


    # 批量插入docu到friends type中
    def insert_friend_docu(self,username,docu_list,doc_type=settings.FRIENDS_TYPE_NAME):
        if self.els_conn.indices.exists(index=username) is True:
            for elem in docu_list:
                self.els_conn.index(index=username,doc_type=doc_type,body=elem)
        else:
            return False#index不存在

    # 批量修改某个用户的多个好友信息
    def modify_docu(self,username,docu_list,doc_type=settings.FRIENDS_TYPE_NAME):
        if self.els_conn.indices.exists(index=username) is True:
            for elem in docu_list:
                query_dict = {
                    'query': {
                        'match': {
                            settings.FRIEND_ID_NAME: username
                        }
                    }
                }
                result = self.els_conn.search(index=username, doc_type=doc_type, body=query_dict)
                print("############################")
                print(result)
        else:
            return False#index不存在

    def query_friend_docu(self,username,query_dict,doc_type=settings.FRIENDS_TYPE_NAME):
        result=self.els_conn.search(index=username,doc_type=doc_type,body=query_dict)
        # 查询得到的result直接就是dict类型
        return result

    def query_update(self,username,query_dict,doc_type,id):
        # 查看更新feature types是否成功
        # print("hahaha")
        result=self.els_conn.update(index=username,doc_type=doc_type,id=id,body=query_dict)
        # print(result)
        return result

    # 通过index/type/id 查询单条document
    def query_by_id(self,username,doc_type,id):
        result=self.els_conn.get(index=username,doc_type=doc_type,id=id)
        return result

    def delete_by_id(self,username,doc_type,id):
        result=self.els_conn.delete(index=username,doc_type=doc_type,id=id)
        return result