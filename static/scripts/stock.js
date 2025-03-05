  $('#restock').on('click', function(){
    var rand_amount = Math.floor(Math.random()*10)

    $.ajax({
      url: '/api/resupply/1?key=1111',
      method: 'PATCH',
      contentType: 'application/json',
      data: JSON.stringify({'amount': rand_amount})
    }).done(function(data){
      $.ajax({
        url: '/stock',
        method: 'GET',
      }).done(function(data){
        $('body').html(data);
      });
    });

    $.ajax({
      url: '/api/resupply/2?key=1111',
      method: 'PATCH',
      contentType: 'application/json',
      data: JSON.stringify({'amount': rand_amount})
    }).done(function(data){
      $.ajax({
        url: '/stock',
        method: 'GET',
      }).done(function(data){
        $('body').html(data);
      });
    });

    $.ajax({
      url: '/api/resupply/3?key=1111',
      method: 'PATCH',
      contentType: 'application/json',
      data: JSON.stringify({'amount': rand_amount})
    }).done(function(data){
      $.ajax({
        url: '/stock',
        method: 'GET',
      }).done(function(data){
        $('body').html(data);
      });
    });

    $.ajax({
      url: '/api/resupply/4?key=1111',
      method: 'PATCH',
      contentType: 'application/json',
      data: JSON.stringify({'amount': rand_amount})
    }).done(function(data){
      $.ajax({
        url: '/stock',
        method: 'GET',
      }).done(function(data){
        $('body').html(data);
      });
    });
  });