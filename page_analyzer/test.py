{% extends 'page_header.html' %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
</head>
<body>
    {% for msg in get_flashed_messages() %}
    <div class="alert alert-danger" role="alert"> {{ msg }} </div>
    {% endfor %}
    <main class="flex-grow-1">
        <div class="container-lg mt-3">
            <div class="row">
                <div class="col-12 col-md-10 col-lg-8 mx-auto border rounded-3 bg-light p-5">
                    <h1 class="display-3"> Анализатор страниц </h1>
                    <p class="lead"> Бесплатно проверяйте сайты на SEO-пригодность </p>
                    <form class="d-flex justify-content-center" style="width 18rem;" method="post">        
                        <input class="form-control form-control-lg" type="text" placeholder="https://www.example.com" name="url" value="" required/>
                        <input class="btn btn-primary  btn-lg ms-3 px-5 text-uppercase mx-3" type="submit" value="ПРОВЕРИТЬ"/>
                    </form>
                </div>
            </div>
        </div>

</body>
</html>



------
{% extends 'page_header.html' %}
{% block content -%}
{{ super() }}

{% for msg in get_flashed_messages() %}
<div class="alert alert-danger" role="alert"> {{ msg }} </div>
{% endfor %}
<main class="flex-grow-1">
    <div class="container-lg mt-3">
        <div class="row">
            <div class="col-12 col-md-10 col-lg-8 mx-auto border rounded-3 bg-light p-5">
                <h1 class="display-3"> Анализатор страниц </h1>
                <p class="lead"> Бесплатно проверяйте сайты на SEO-пригодность </p>
                <form class="d-flex justify-content-center" style="width 18rem;" method="post">        
                    <input class="form-control form-control-lg" type="text" placeholder="https://www.example.com" name="url" value="" required/>
                    <input class="btn btn-primary  btn-lg ms-3 px-5 text-uppercase mx-3" type="submit" value="ПРОВЕРИТЬ"/>
                </form>
            </div>
        </div>
    </div>
{% endblock -%}
