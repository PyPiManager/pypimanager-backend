# alembic 

##　初始化

###　1. 生成
```shell
alembic init migrations
```

### 2. 修改
- alembic.ini
  - `sqlalchemy.url`
- migrations/env.py
  - `target_metadata`

## 使用
```
alembic revision --autogenerate -m "init db"
alembic upgrade head
alembic downgrade "xxx"
```