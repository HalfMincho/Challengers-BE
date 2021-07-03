Challenge api
======================

/challenge/(int:challenge_id) (GET)
-------------------------------------

    **Get information of challenge**

    :Paramaters:

        **challenge_id**

        - name: challenge_id
        - in: path
        - description: challenge ID
        - required: true


    **Example request**:

    .. sourcecode:: http

        GET /challenge/1 HTTP/1.1
        Host: api.challengers.halfmincho.com
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
            "auth_count_in_day": 1,
            "auth_day": "0000002",
            "auth_way": 1,
            "category": "874fc780-2bbf-4578-94c0-dfb9167e4015",
            "cost": 1000,
            "description": "test_description",
            "end_at": "Sat, 05 Jun 2021 21:42:01 GMT",
            "id": 1,
            "name": "test_name",
            "reg_date": "Sat, 05 Jun 2021 21:42:01 GMT",
            "start_at": "Sat, 05 Jun 2021 21:42:01 GMT",
            "submitter": "874fc780-2bbf-4578-94c0-dfb9167e4015",
            "views": 13
        }

    :resheader Content-Type: application/json
    :status:
        - 200: challenge found
        - 404: challenge no exists
    :returns: information of challenge


/challenge (POST)
------------------------

    **Add new challenge to db**

    :Parameters:

        **submitter**

        - name: submitter
        - in: query
        - description: challenge 작성자
        - required: true

        **category**

        - name: category
        - in: query
        - description: challenge category
        - required: true

        **name**

        - name: name
        - in: query
        - description: 새 challenge의 게시판 이름
        - required: true

        **auth_way**

        - name: auth_way
        - in: query
        - description: challenge 인증 방법
        - required: true

        **auth_day**

        - name: auth_day
        - in: query
        - description: challenge 인증 요일
        - required: true

        **auth_count_in_day**

        - name: auth_count_in_day
        - in: query
        - description: challenge 하루 인증 횟수
        - required: true

        **start_at**

        - name: start_at
        - in: query
        - description: challenge 시작 날짜
        - required: true

        **end_at**

        - name: end_at
        - in: query
        - description: challenge 마감 날짜
        - required: true

        **cost**

        - name: cost
        - in: query
        - description: 비용
        - required: true

        **title_image**

        - name: title_image
        - in: query
        - description: 대표 이미지
        - required: true

        **description**

        - name: description
        - in: query
        - description: challenge 설명
        - required: true

    **Example request**:

    .. sourcecode:: http

        POST /challenge HTTP/1.1
        Host: api.challengers.halfmincho.com
        Accept: application/json
        Content-Type: application/json

        {
            "submitter": "hi",
            "category": "test_category",
            "name": "name33232",
            "auth_way": 5,
            "auth_day": "0000010",
            "auth_count_in_day": 1,
            "start_at": "test_start_at",
            "end_at": "test_end_at",
            "cost": 103000,
            "title_image": "",
            "description": "description"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept

    :resheader Content-Type: application/json
    :status:
        - 200: add challenge completely
        - 400: no required arguments

/challenge/popular (GET)
------------------------

    **Get 10 popular challenges**

    view가 가장 많은 10개의 challenge를 가져옴

    :Parameters:

        **No required parameters**


    **Example request**:

    .. sourcecode:: http

        GET /challenge/popular HTTP/1.1
        Host: api.challengers.halfmincho.com
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

            [
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 1,
                    "category": "874fc780-2bbf-4578-94c0-dfb9167e4015",
                    "cost": 1000,
                    "description": "test_description",
                    "end_at": "Sat, 05 Jun 2021 21:42:01 GMT",
                    "id": 1,
                    "name": "test_name",
                    "reg_date": "Sat, 05 Jun 2021 21:42:01 GMT",
                    "start_at": "Sat, 05 Jun 2021 21:42:01 GMT",
                    "submitter": "874fc780-2bbf-4578-94c0-dfb9167e4015",
                    "views": 13
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "8bc28cfc-1bf0-44ca-9af3-86850ef37104",
                    "cost": 10000,
                    "description": "test_description",
                    "end_at": "Sun, 06 Jun 2021 21:09:14 GMT",
                    "id": 2,
                    "name": "test_name",
                    "reg_date": "Sun, 06 Jun 2021 21:09:14 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:14 GMT",
                    "submitter": "8bc28cfc-1bf0-44ca-9af3-86850ef37104",
                    "views": 3
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000010",
                    "auth_way": 2,
                    "category": "e8acab40-4ebc-4fc3-949c-8fde812c647c",
                    "cost": 103000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:10:54 GMT",
                    "id": 10,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:54 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:54 GMT",
                    "submitter": "e8acab40-4ebc-4fc3-949c-8fde812c647c",
                    "views": 2
                },
                {
                    "auth_count_in_day": 2,
                    "auth_day": "0000010",
                    "auth_way": 1,
                    "category": "40f89f9e-e973-4df3-b719-2810a1640dc0",
                    "cost": 12000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:10:35 GMT",
                    "id": 8,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:35 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:35 GMT",
                    "submitter": "40f89f9e-e973-4df3-b719-2810a1640dc0",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "5536068e-2667-4c3c-a41c-421f040f7a42",
                    "cost": 5000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:09:41 GMT",
                    "id": 4,
                    "name": "name123",
                    "reg_date": "Sun, 06 Jun 2021 21:09:41 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:41 GMT",
                    "submitter": "5536068e-2667-4c3c-a41c-421f040f7a42",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000010",
                    "auth_way": 2,
                    "category": "7c6faa14-615b-4018-b068-300fdf5d4b44",
                    "cost": 100000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:10:49 GMT",
                    "id": 9,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:49 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:49 GMT",
                    "submitter": "7c6faa14-615b-4018-b068-300fdf5d4b44",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "ae9961f2-0d1f-4b86-9554-6765ea36f364",
                    "cost": 7000,
                    "description": "test-description",
                    "end_at": "Sun, 06 Jun 2021 21:09:51 GMT",
                    "id": 5,
                    "name": "name123222",
                    "reg_date": "Sun, 06 Jun 2021 21:09:51 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:51 GMT",
                    "submitter": "ae9961f2-0d1f-4b86-9554-6765ea36f364",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "b9c9a28b-15e8-4610-b051-057ff0fb690e",
                    "cost": 3000,
                    "description": "test_description",
                    "end_at": "Sun, 06 Jun 2021 21:09:32 GMT",
                    "id": 3,
                    "name": "name",
                    "reg_date": "Sun, 06 Jun 2021 21:09:32 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:32 GMT",
                    "submitter": "b9c9a28b-15e8-4610-b051-057ff0fb690e",
                    "views": 1
                },
                {
                    "auth_count_in_day": 2,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "becf925c-5f21-4a4d-9db1-675c8ffef69c",
                    "cost": 12000,
                    "description": "test-description",
                    "end_at": "Sun, 06 Jun 2021 21:10:14 GMT",
                    "id": 6,
                    "name": "name2",
                    "reg_date": "Sun, 06 Jun 2021 21:10:14 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:14 GMT",
                    "submitter": "becf925c-5f21-4a4d-9db1-675c8ffef69c",
                    "views": 1
                },
                {
                    "auth_count_in_day": 2,
                    "auth_day": "0000000",
                    "auth_way": 3,
                    "category": "c161892d-a5a2-45fe-b0db-3788e98bfe7a",
                    "cost": 12000,
                    "description": "test-description",
                    "end_at": "Sun, 06 Jun 2021 21:10:23 GMT",
                    "id": 7,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:23 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:23 GMT",
                    "submitter": "c161892d-a5a2-45fe-b0db-3788e98bfe7a",
                    "views": 1
                }
            ]

    :resheader Content-Type: application/json
    :status:
        - 200: success
        - 404: challenge가 존재하지 않음
    :returns: list of challenges


/challenge/recent (GET)
-----------------------

    **Get 10 recent challenges**

    가장 최근에 생성된 10개의 challenge를 반환

    :Parameters:

        **No required parameters**


    **Example request**:

    .. sourcecode:: http

        GET /challenge/recent HTTP/1.1
        Host: api.challengers.halfmincho.com
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

            [
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000010",
                    "auth_way": 5,
                    "category": "dfb28fd9-48f1-400f-8112-5b8b5cf98aa0",
                    "cost": 103000,
                    "description": "description",
                    "end_at": "Tue, 22 Jun 2021 15:58:56 GMT",
                    "id": 11,
                    "name": "name33232",
                    "reg_date": "Tue, 22 Jun 2021 15:58:56 GMT",
                    "start_at": "Tue, 22 Jun 2021 15:58:56 GMT",
                    "submitter": "dfb28fd9-48f1-400f-8112-5b8b5cf98aa0",
                    "views": 0
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000010",
                    "auth_way": 2,
                    "category": "e8acab40-4ebc-4fc3-949c-8fde812c647c",
                    "cost": 103000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:10:54 GMT",
                    "id": 10,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:54 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:54 GMT",
                    "submitter": "e8acab40-4ebc-4fc3-949c-8fde812c647c",
                    "views": 2
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000010",
                    "auth_way": 2,
                    "category": "7c6faa14-615b-4018-b068-300fdf5d4b44",
                    "cost": 100000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:10:49 GMT",
                    "id": 9,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:49 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:49 GMT",
                    "submitter": "7c6faa14-615b-4018-b068-300fdf5d4b44",
                    "views": 1
                },
                {
                    "auth_count_in_day": 2,
                    "auth_day": "0000010",
                    "auth_way": 1,
                    "category": "40f89f9e-e973-4df3-b719-2810a1640dc0",
                    "cost": 12000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:10:35 GMT",
                    "id": 8,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:35 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:35 GMT",
                    "submitter": "40f89f9e-e973-4df3-b719-2810a1640dc0",
                    "views": 1
                },
                {
                    "auth_count_in_day": 2,
                    "auth_day": "0000000",
                    "auth_way": 3,
                    "category": "c161892d-a5a2-45fe-b0db-3788e98bfe7a",
                    "cost": 12000,
                    "description": "test-description",
                    "end_at": "Sun, 06 Jun 2021 21:10:23 GMT",
                    "id": 7,
                    "name": "name332",
                    "reg_date": "Sun, 06 Jun 2021 21:10:23 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:23 GMT",
                    "submitter": "c161892d-a5a2-45fe-b0db-3788e98bfe7a",
                    "views": 1
                },
                {
                    "auth_count_in_day": 2,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "becf925c-5f21-4a4d-9db1-675c8ffef69c",
                    "cost": 12000,
                    "description": "test-description",
                    "end_at": "Sun, 06 Jun 2021 21:10:14 GMT",
                    "id": 6,
                    "name": "name2",
                    "reg_date": "Sun, 06 Jun 2021 21:10:14 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:10:14 GMT",
                    "submitter": "becf925c-5f21-4a4d-9db1-675c8ffef69c",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "ae9961f2-0d1f-4b86-9554-6765ea36f364",
                    "cost": 7000,
                    "description": "test-description",
                    "end_at": "Sun, 06 Jun 2021 21:09:51 GMT",
                    "id": 5,
                    "name": "name123222",
                    "reg_date": "Sun, 06 Jun 2021 21:09:51 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:51 GMT",
                    "submitter": "ae9961f2-0d1f-4b86-9554-6765ea36f364",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "5536068e-2667-4c3c-a41c-421f040f7a42",
                    "cost": 5000,
                    "description": "description",
                    "end_at": "Sun, 06 Jun 2021 21:09:41 GMT",
                    "id": 4,
                    "name": "name123",
                    "reg_date": "Sun, 06 Jun 2021 21:09:41 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:41 GMT",
                    "submitter": "5536068e-2667-4c3c-a41c-421f040f7a42",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "b9c9a28b-15e8-4610-b051-057ff0fb690e",
                    "cost": 3000,
                    "description": "test_description",
                    "end_at": "Sun, 06 Jun 2021 21:09:32 GMT",
                    "id": 3,
                    "name": "name",
                    "reg_date": "Sun, 06 Jun 2021 21:09:32 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:32 GMT",
                    "submitter": "b9c9a28b-15e8-4610-b051-057ff0fb690e",
                    "views": 1
                },
                {
                    "auth_count_in_day": 1,
                    "auth_day": "0000002",
                    "auth_way": 3,
                    "category": "8bc28cfc-1bf0-44ca-9af3-86850ef37104",
                    "cost": 10000,
                    "description": "test_description",
                    "end_at": "Sun, 06 Jun 2021 21:09:14 GMT",
                    "id": 2,
                    "name": "test_name",
                    "reg_date": "Sun, 06 Jun 2021 21:09:14 GMT",
                    "start_at": "Sun, 06 Jun 2021 21:09:14 GMT",
                    "submitter": "8bc28cfc-1bf0-44ca-9af3-86850ef37104",
                    "views": 3
                }
            ]

    :resheader Content-Type: application/json
    :status:
        - 200: success
        - 404: challenge가 존재하지 않음
    :returns: list of challenges