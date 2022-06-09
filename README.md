**cx_Oracle installation for Mac:**

```
1)instantclient oracle sitesinden indirilir. 
instantclient_19_8 unzip edilir ve elzem değil ama best practise oalarak aşağıdaki path altına koyulur.
 /opt/oracle
```

```
2) Projenin içerisinde örneği yer alan ve bağlantı bilgilerinin tutulduğu tnsnames.ora
dosyası instantclient'ın içerisinde yer alan /network/admin dizinine yapıştırlır.
Bu işlem sonunda aşağıdaki çıktıyı görmeliyiz

/opt/oracle/instantclient_19_8/network/admin/tnsnames.ora
```

``` 
3).bash_profile 'de aşağıdaki değişkenler tanımlanır. 
      export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_8
      export TNS_ADMIN = $LD_LIBRARY_PATH/network/admin
```

```
4)Şayet /etc/hosts dosyasında 
127.0.0.1 Mac111019 
   yazmıyorsa, yazılır.Buradaki 'Mac111019' ibaresini öğrenmek için
   terminale 'hostname' komutu yazılır.
```

```
5) tnsnames.ora'nın da aşağıdaki formatta olması gerekmektedir.

QA_N11 =
   (DESCRIPTION=
      (ADDRESS=(PROTOCOL=tcp)(HOST=host.name.qa)(PORT=1523))
      (CONNECT_DATA= (SERVICE_NAME=serviceName))
   )
   TEST_N11 =
   (DESCRIPTION=
      (ADDRESS=(PROTOCOL=tcp)(HOST=host.name.test)(PORT=1523))
      (CONNECT_DATA= (SERVICE_NAME=serviceName))
   )
   ST_N11 =
   (DESCRIPTION=
      (ADDRESS=(PROTOCOL=tcp)(HOST=host.name.st)(PORT=1523))
      (CONNECT_DATA= (SERVICE_NAME=serviceName))
   )
```

**psycopg2 installation for Mac:**

```
1) Postgres server aşağıdaki linkten indirilir.
https://postgresapp.com/downloads.html
Ardından kurulum yapılır. 
```

```
2) Postgres uygulamasının binary'leri .bash_profile'de $PATH değişkenine eklenir
Not: Uygulamanın versiyonuna değişiklik gösterebilir.

 ls /Applications/Postgres.app/Contents/Versions/
 
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/14/bin
```

```
3) Ardından sırası ile ilk önce postgres ardından psycopg2 paketleri indirilir
 pip3 install postgres
 pip3 install psycopg2
```

**Yeni Servis Eklenmesi**

1) `tdm/flask_app/all_services` altına yeni servis grubu eklenir. Örn: `tdm/flask_app/all_services/visitor_servise`
2) Eklenilen servisin routes.py ve utils.py class'ları implemente edilir.
3) Eklenen servis swagger'da listelenebilmesi için
   `tdm/flask_app/all_services/visitor_service/swagger_yml_files/create_visitor.yml` .yml implementasyonu yapılır.
4) Eklenen yeni servisin blueprint registration'u yapılmalıdır.
   `tdm/flask_app/all_services/__init__.py` içerisinde yer alan create_app methodu içine eklemeyi unutmayalım
   ```
   def create_app():
    from tdm.flask_app.all_services.common_service.routes import common_service
    app.register_blueprint(common_service)
   ```