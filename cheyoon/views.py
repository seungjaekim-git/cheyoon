import json
import math
import datetime

from django.http      import JsonResponse,HttpResponse
from django.views     import View
from django.db.models import Q

class HomeView(View):      
    def get(self, request, board_pk):
        try :
            
            #api 주소 : 승재 노트북 주소/homes/번호
            #ex ) 0.0.0.0:8000/homes/1
            #http method : get
            #1번 숙소에 대한 디테일 정보 조회 api 요청시 아래와 같은 데이터가 전송될거예요

            data ={
                "room_id" : 1,
                "name" : "[V-2]♥자가격리 가능♥[아트하우스]♥선정릉역앞",
                "address" : "강남구, 서울, 한국",
                "images" : ["https://a0.muscache.com/im/pictures/aa6a8577-ddc1-4543-af64-18bf7aa296fe.jpg?im_w=1200" , "https://a0.muscache.com/im/pictures/51e3a0de-4c9e-44a2-b0bd-c94c324453b1.jpg?im_w=720", "https://a0.muscache.com/im/pictures/d0e1fb79-4d78-42b3-8c00-f53ad92a04f2.jpg?im_w=720" , "https://a0.muscache.com/im/pictures/8c331579-3c6a-4098-be3a-70cd4314a6b5.jpg?im_w=720", "https://a0.muscache.com/im/pictures/f88e246f-3d84-4a87-8a25-6b3681cc3c28.jpg?im_w=720"],
                "capacity" : 4,
                "options" : {
                            "bedroom" : 2,
                            "bed" : 1,
                            "bathroom" : 1
                            },
                "home_type" : "집 전체",
                "description" : "서울, 경기 전역 자가격리 객실 다량 확보되어있습니다.안녕하세요",
                "host" : {

                    "host_id" :1,
                    "host_name" : "김승재",
                    "host_description" : "안녕하세요.내 집같이 편안한 숙소를 제공하고 있습니다.",
                    "contact" : "010-8888-8888",
                    "email" : "sj950902@naver.com",
                    "is_valid" : 1,
                    "signup_date" : "2020-10-11"
                },

                "facility_detail" : {
                    
                    "bathroom" : ["헤어드라이어"],
                    "general" : ["주방","무선인터넷"],
                    "entertainment" : ["TV","Playstation"]
                },

                "facility_list" : [
                    {
                        "name" : "욕실",
                        "url"  : "data:image/png;base64,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"
                    },
                    {
                        "name" : "주방",
                        "url " : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJI3x2kuAJg9KdC4yRW9zoUS_q4TXDUGR79w&usqp=CAU"
                    },
                    {
                        "name" : "TV",
                        "url" :  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPsAAADJCAMAAADSHrQyAAAAaVBMVEX///8AAAD09PT5+flLS0vPz8/f39+ZmZmoqKgWFhZ2dnbt7e36+vpnZ2fT09PJyckhISG5ubk1NTWvr6+/v7/o6Og6OjoICAipqakPDw95eXlYWFiWlpZBQUGPj49TU1OCgoIqKipwcHAmIPpdAAAC2UlEQVR4nO3diVLiQBhF4YyETghrWOKIuL7/Q45IOUGlgUAnl+4+5wHG/6tIpheqTJL9TF6kgz9hNkiL3CSWelmo7LpB1jtEz9RzddTml9zM1DN11uzHb36pHqjTyn16rp6m4/JYn/q2/0/eqCcR9PWZj+c1VzeL6z+372WfSxr1FKJ60T723YMPfyF7uEGcL/ldJrplTd3fpFCPIKtIUvUIstJoX3Xbl516AmHY4wx7nGGPM7t9eBdGwwvsI9sdhmeNLrAfvMDwMPvZDHbs2LFjDyHs2LFjx44dO3bsYYQdO3bs2LFjx449jLBjx44dO3bs2LGHEXbs2LFjx44dO/Ywwo4dO3bs2LFjxx5G2LFjx44dO3bs2MMIO3bs2LFjx44dexhhx44dO3bs2LFjDyPs2LFjx44dO3bsYYQdO3bs2LFjx449jLBjx37arp7ZWRfY01C6wB5+2OMMe5xFbX9QTyDrIZmrR5A1T8bqEWSNk0w9gqws6atHkNU/stQPvY9tzlo9g6j1h92ohxBltvvbON/048+9vf2Pw4fccHewsVDPIWjxdapTqCfpvKI+0npUz9Jxj/vneXG978bfDzNjWtpmP09yTSwburk5cI69rNRjdVC1tJzim82TerZWe9oceuZ1q0m/5abW2aZt/tjJ6qi7m0ZW+0g9WuvZLwdDuf60hx07duzYww57nHb7us4D+9112c9Gh1f+yy27zfMt73Sr5+MbtWtavah1J3tpabuWq2FnlbdBf1WrzuzVPd2f48xfh5HXNlGLGjRxbH9Tgxr05pZuP2W7xaZO7X7d3IxPgxqk1jTMJd23b2e4XN/59XF3+4FfqjENs109XZJvX8Nz+dxXakzDnO5o1JiGuaQn72pNo96d2n1azjtf0Pt0NZ+6pXv1tnN+dlOqRWe3OI1pmh9HVi0dWvmxsHW5pNurd/tftl+3d8HRK4vqXu2zdF+tyybyfwbibFbfJf4YAAAAAElFTkSuQmCC"
                    }
                ],

                "facility_hardmode" : [

                    {
                        "category" : "욕실용",
                        "name" : "욕실",
                        "url"  : "data:image/png;base64,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"

                    },
                    {
                        "category" : "기본옵션",
                        "name" : "주방",
                        "url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJI3x2kuAJg9KdC4yRW9zoUS_q4TXDUGR79w&usqp=CAU"
                    },{
                        "category" : "엔터테인먼트",
                        "name" : "TV",
                        "url" :  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPsAAADJCAMAAADSHrQyAAAAaVBMVEX///8AAAD09PT5+flLS0vPz8/f39+ZmZmoqKgWFhZ2dnbt7e36+vpnZ2fT09PJyckhISG5ubk1NTWvr6+/v7/o6Og6OjoICAipqakPDw95eXlYWFiWlpZBQUGPj49TU1OCgoIqKipwcHAmIPpdAAAC2UlEQVR4nO3diVLiQBhF4YyETghrWOKIuL7/Q45IOUGlgUAnl+4+5wHG/6tIpheqTJL9TF6kgz9hNkiL3CSWelmo7LpB1jtEz9RzddTml9zM1DN11uzHb36pHqjTyn16rp6m4/JYn/q2/0/eqCcR9PWZj+c1VzeL6z+372WfSxr1FKJ60T723YMPfyF7uEGcL/ldJrplTd3fpFCPIKtIUvUIstJoX3Xbl516AmHY4wx7nGGPM7t9eBdGwwvsI9sdhmeNLrAfvMDwMPvZDHbs2LFjDyHs2LFjx44dO3bsYYQdO3bs2LFjx449jLBjx44dO3bs2LGHEXbs2LFjx44dO/Ywwo4dO3bs2LFjxx5G2LFjx44dO3bs2MMIO3bs2LFjx44dexhhx44dO3bs2LFjDyPs2LFjx44dO3bsYYQdO3bs2LFjx449jLBjx37arp7ZWRfY01C6wB5+2OMMe5xFbX9QTyDrIZmrR5A1T8bqEWSNk0w9gqws6atHkNU/stQPvY9tzlo9g6j1h92ohxBltvvbON/048+9vf2Pw4fccHewsVDPIWjxdapTqCfpvKI+0npUz9Jxj/vneXG978bfDzNjWtpmP09yTSwburk5cI69rNRjdVC1tJzim82TerZWe9oceuZ1q0m/5abW2aZt/tjJ6qi7m0ZW+0g9WuvZLwdDuf60hx07duzYww57nHb7us4D+9112c9Gh1f+yy27zfMt73Sr5+MbtWtavah1J3tpabuWq2FnlbdBf1WrzuzVPd2f48xfh5HXNlGLGjRxbH9Tgxr05pZuP2W7xaZO7X7d3IxPgxqk1jTMJd23b2e4XN/59XF3+4FfqjENs109XZJvX8Nz+dxXakzDnO5o1JiGuaQn72pNo96d2n1azjtf0Pt0NZ+6pXv1tnN+dlOqRWe3OI1pmh9HVi0dWvmxsHW5pNurd/tftl+3d8HRK4vqXu2zdF+tyybyfwbibFbfJf4YAAAAAElFTkSuQmCC"
                    }
                ],
                
                "rules" : 

                     [{
                        "category" : "숙소이용규칙",
                        "name" : "흡연금지",
                        "description" : None

                    },{

                         "category" : "숙소이용규칙",
                        "name" : "반려동물 동분 불가",
                        "description" : None      

                    },{

                        "category" : "건강과 안전",
                        "name" : "에어비앤비의 사회적 거리 두기 및 관련 가이드라인이 적용됩니다.",
                        "description" : None

                    },
                      {
                        "category" : "환불정책",
                        "name" : "체크인 24시간 전까지 수수료 없이 예약 취소 가능",
                        "description" : None

                      }
                ]
            }


            
            return JsonResponse(data, status=200)


        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "INVALID_DATA"}, status=400)




