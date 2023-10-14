{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block content %}

<div class="header-bar">
    <h1>Register</h1>
</div>

<div class="card-body">
    <form method="POST">
        {% csrf_token %}
      <p>  <label>{{form.username.label}}</label>
        {{form.username}}</p>

       <p> <label>{{form.password1.label}}</label>
        {{form.password1}}</p>

       <p> <label>{{form.password2.label}}</label>
        {{form.password2}}</p>
        <input style="margin-top:10px ;" class="button" type="submit" value="Register">
    </form>
    
</div>

<div class="row" style="color: #0d6efd; font-style: bold; font-size: 1rem; ">
    <div class="col-md-6"><p>Already have an account? <a href="{% url 'accounts:login' %}">Login</a></p></div>
    
    <div class="col-md-6"> <p>For any issues or concerns information, please  <a href="{% url 'accounts:contact' %}">Contact us</a></p></div>
   
    
</div>

{% endblock content %}