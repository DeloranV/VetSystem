 $('#add_app').on('click', function(){
        if($('#type_select').length == 0) {

          var $type_label = $('<label>Rodzaj wizyty</label>');
          var $type_select = $('<select>')
          .attr('id', 'type_select');

          var $kontrola_option = $('<option value="k">Kontrola</option>');
          var $zabieg_option = $('<option value="z">Zabieg</option>');
          var $dolegliwosc_option = $('<option value="d">Dolegliwość</option>');

          var $pet_label = $('<label>Zwierzę do zarejestrowania</label>');
          var $pet_input = $('<input>')
          .attr('id', 'pet_input')
          .attr('type', 'text');

          var $scheduled_label = $('<label>Termin wizyty</label>');
          var $scheduled_input = $('<input>')
          .attr('id', 'scheduled_input')
          .attr('type', 'text')
          .attr('placeholder','RRRR-MM-DD HH:MM:SS');

          var $submit_button = $('<input>')
          .attr('type', 'button')
          .attr('id', 'submit_button')
          .attr('value', 'Zarejestruj');

          $('#register_container').append($type_label, $type_select, $pet_label, $pet_input, $scheduled_label,
                          $scheduled_input, $submit_button);

          $('#type_select').append($kontrola_option, $zabieg_option, $dolegliwosc_option);

          $('#submit_button').on('click', function(){

            var $type_val = $('#type_select').val();
            var $pet_val = $('#pet_input').val();
            var $scheduled_val = $('#scheduled_input').val();

            $.ajax({
              url: '/api/appointments'.concat('?key=1111'),
              method: 'POST',
              contentType: 'application/json',
              data: JSON.stringify({"pet_id": $pet_val,
                                    "appointment_type": $type_val,
                                    "scheduled": $scheduled_val})
            }).done(function(data){
              $.ajax({
                url: '/appointments',
                method: 'GET',

              }).done(function(data){
                $('body').html(data);
              });
            });
          });
        };
    });

