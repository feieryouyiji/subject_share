### 有关orm的小实践

#### 介绍
- ORM，Object-Relational Mapping（对象关系映射，它的作用是在关系型数据库和业务实体对象之间作一个映射，这样，我们在具体的操作业务对象的时候，就不需要再去和复杂的SQL语句打交道，只需简单的操作对象的属性和方法，sql语句的一种抽象。

#### 为什么需要ORM

```
UPDATE table_name SET column1 = value1, column2 = value2....columnN=valueN [ WHERE  CONDITION ];

user.update(...)

```

- 优点
    - 简洁易读
    - 复用可维护
    - 开发效率高
- 缺点
    - 不太容易处理复杂查询语句
    - 性比sql差

### 编写orm

