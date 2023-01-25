$(document).ready(function () {
     $('#showpwd').on('click', function () {
          if ($('#pwd').attr('type') == 'password') {
               $('#pwd').attr('type', 'text');
          }
          else {
               $('#pwd').attr('type', 'password');
          }
     });
     $('#showpwd1').on('click', function () {
          if ($('#pwd').attr('type') == 'password1') {
               $('#pwd').attr('type', 'text');
          }
          else {
               $('#pwd').attr('type', 'password');
          }
     });
     $('#showpwd2').on('click', function () {
          if ($('#pwd').attr('type') == 'password2') {
               $('#pwd').attr('type', 'text');
          }
          else {
               $('#pwd').attr('type', 'password');
          }
     });
     $("#search").on('keyup', function () {
          var search = $(this).val().toLowerCase();
          $('#data tbody tr').filter(function () {
               $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
          });
     });
});