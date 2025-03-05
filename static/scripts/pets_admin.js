$('#remove_pet').on('click', function(){
      var $pet_id = $('#remove_id').val();

      $.ajax({
        url: '/api/pets/'.concat($pet_id, '?key=1111'),
        method: 'DELETE'
      }).done(function(data){
        $.ajax({
          url: '/pets',
          method: 'GET'
        }).done(function(data){
          $('body').html(data);
        });
      });
    });