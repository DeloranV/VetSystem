   $('#change_submit').on('click', function(){
        $name_val = $('#name').val();
        $surname_val = $('#surname').val();
        $email_val = $('#email').val();
        $phone_val = $('#phone').val();

        data_object = {"name": $name_val,
                       "surname": $surname_val,
                       "email": $email_val,
                       "phone": $phone_val}

        $.ajax({
            url: '/api/account?key=1111',
            method: 'PATCH',
            contentType: 'application/json',
            data: JSON.stringify(data_object)
        }).success(function(data){
            $.ajax({
                url: '/account',
                method: 'GET'
            }).done(function(data){
                $('body').html(data);
                $('#result_box').append("<p>Pomyślnie zaaktualizowano dane</p>")
            });
        }).error(function(data){
            $('#result_box').append("Nie udało się zaaktualizować danych");
        });
    });