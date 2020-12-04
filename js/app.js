$('#songCarousel').carousel({
  interval :0
})

// default 2 displays 4 carousel items
let carouselDisplay = 2;

// displays 3 carousel items if viewport width less than 1650px
if(document.documentElement.clientWidth < 1650) {
  carouselDisplay = 1
}

// // displays 2 carousel items if viewport width less than 1320px
if(document.documentElement.clientWidth < 1320) {
  carouselDisplay = 0
}

$('.carousel .carousel-item').each(function(){
    // if the viewport width is less than 840, none of this runs and it stays
    // a standard carousel
    if(document.documentElement.clientWidth > 840){
      
      var next = $(this).next();

      if (!next.length) {
        next = $(this).siblings(':first');
      }

      next.children(':first-child').clone().appendTo($(this));
      
      for (var i=0;i<carouselDisplay;i++) {

          next = next.next();

          if (!next.length) {
            next = $(this).siblings(':first');
          }
          
          next.children(':first-child').clone().appendTo($(this));
        }
    }
});

$(window).resize(function() {
  console.log('window was resized');
  console.log(document.documentElement.clientWidth)
  if(document.documentElement.clientWidth >= 1650) {
    carouselDisplay = 2
  }
  if(document.documentElement.clientWidth < 1650) {
    carouselDisplay = 1
    // $('.carousel .carousel-item').each(function(){
    //   console.log($(this).children().children().children())
    // })
  }
  if(document.documentElement.clientWidth < 1320) {
    carouselDisplay = 0
  }
  console.log(carouselDisplay)
});