CREATE TABLE app_user (
  user_id          NUMBER(10)       NOT NULL,
  email            VARCHAR2(200 CHAR) NOT NULL,
  password         VARCHAR2(100 CHAR) NOT NULL,
  name             VARCHAR2(50 CHAR)  NOT NULL,
  gender           CHAR(5 CHAR)       NOT NULL,
  birth_date       CHAR(20 CHAR)      NOT NULL,
  created_at       DATE              DEFAULT SYSDATE NOT NULL,
  CONSTRAINT pk_app_user PRIMARY KEY (user_id)
);

CREATE TABLE user_preference (
  preference_id    NUMBER(10)       NOT NULL,
  user_id          NUMBER(10)       NOT NULL,
  theme            VARCHAR2(100 CHAR) NOT NULL,
  duration         VARCHAR2(50 CHAR)  NOT NULL,
  region           VARCHAR2(100 CHAR) NOT NULL,
  CONSTRAINT pk_user_pref PRIMARY KEY (preference_id),
  CONSTRAINT fk_pref_user FOREIGN KEY (user_id) REFERENCES app_user(user_id)
);


CREATE TABLE itinerary (
  itinerary_id     NUMBER(10)       NOT NULL,
  preference_id    NUMBER(10)       NOT NULL,
  user_id          NUMBER(10)       NOT NULL,
  start_date       DATE             NOT NULL,
  end_date         DATE             NOT NULL,
  created_at       DATE             DEFAULT SYSDATE NOT NULL,
  is_deleted       NUMBER(1)        DEFAULT 0 NOT NULL,   
  CONSTRAINT pk_itinerary PRIMARY KEY (itinerary_id),
  CONSTRAINT fk_itin_pref FOREIGN KEY (preference_id) REFERENCES user_preference(preference_id),
  CONSTRAINT fk_itin_user FOREIGN KEY (user_id) REFERENCES app_user(user_id)
);

CREATE TABLE place (
  place_id         NUMBER(10)       NOT NULL,
  name             VARCHAR2(100 CHAR) NOT NULL,
  theme            VARCHAR2(80 CHAR)  NOT NULL,
  avg_rating       NUMBER(3,2),
  address          VARCHAR2(200 CHAR) NOT NULL,
  latitude         DECIMAL(9,6)     NOT NULL,
  longitude        DECIMAL(9,6)     NOT NULL,
  description      CLOB,
  heritage_type    VARCHAR2(50 CHAR),
  info_center      VARCHAR2(100 CHAR),
  closed_day       VARCHAR2(20 CHAR),
  experience_info  CLOB,
  min_age          VARCHAR2(10 CHAR),
  business_hours   VARCHAR2(100 CHAR),
  parking_info     VARCHAR2(100 CHAR),
  details          CLOB,
  CONSTRAINT pk_place PRIMARY KEY (place_id)
);
alter table place MODIFY (min_age VARCHAR2(20 char));

CREATE TABLE place_image (
  place_image_id   NUMBER(10)       NOT NULL,
  place_id         NUMBER(10)       NOT NULL,
  has_image        NUMBER(1)        NOT NULL,             -- 0: 없음, 1: 있음
  image_url        VARCHAR2(200 CHAR),
  CONSTRAINT pk_place_image PRIMARY KEY (place_image_id, place_id),
  CONSTRAINT fk_place_image_place FOREIGN KEY (place_id)
    REFERENCES place(place_id)
);


CREATE TABLE schedule_slot (
  slot_id          NUMBER(10)       NOT NULL,
  itinerary_id     NUMBER(10)       NOT NULL,
  place_id         NUMBER(10)       NOT NULL,
  travel_date      DATE             NOT NULL,
  CONSTRAINT pk_schedule_slot PRIMARY KEY (slot_id),
  CONSTRAINT fk_slot_itinerary FOREIGN KEY (itinerary_id) REFERENCES itinerary(itinerary_id),
  CONSTRAINT fk_slot_place FOREIGN KEY (place_id) REFERENCES place(place_id)
);

