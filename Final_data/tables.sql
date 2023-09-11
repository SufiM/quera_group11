create table if not exists currency
(
    id                 int auto_increment
        primary key,
    name               varchar(255) null,
    symbol             varchar(255) null,
    `rank`             int          null,
    main_link          text         null,
    historical_link    text         null,
    circulating_supply double       null
);

create table if not exists github
(
    id                 int auto_increment
        primary key,
    currency_id        int  null,
    commits_count      int  null,
    contributors_count int  null,
    forks_count        int  null,
    stars_count        int  null,
    github_link        text null,
    constraint id
        unique (id),
    constraint github_currency_id_fk
        foreign key (currency_id) references currency (id)
);

create table if not exists historical
(
    id          int auto_increment
        primary key,
    currency_id int      null,
    timeOpen    datetime null,
    timeClose   datetime null,
    timeHigh    datetime null,
    timeLow     datetime null,
    open        double   null,
    high        double   null,
    low         double   null,
    close       double   null,
    volume      double   null,
    marketCap   double   null,
    timestamp   datetime null,
    constraint historical_currency_id_fk
        foreign key (currency_id) references currency (id)
);

create table if not exists languages
(
    id   int          not null
        primary key,
    name varchar(255) null
);

create table if not exists languages_currency
(
    id          int auto_increment
        primary key,
    currency_id int    null,
    language_id int    null,
    percentage  double null,
    constraint id
        unique (id),
    constraint languages_currency_currency_id_fk
        foreign key (currency_id) references currency (id),
    constraint languages_currency_languages_id_fk
        foreign key (language_id) references languages (id)
);

create table if not exists tags
(
    id   int          not null
        primary key,
    name varchar(255) null
);

create table if not exists tags_currency
(
    id          int auto_increment
        primary key,
    currency_id int null,
    tag_id      int null,
    constraint id
        unique (id),
    constraint tags_currency_currency_id_fk
        foreign key (currency_id) references currency (id),
    constraint tags_currency_tags_id_fk
        foreign key (tag_id) references tags (id)
);

