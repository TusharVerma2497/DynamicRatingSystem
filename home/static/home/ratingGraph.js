
values=obj.rating;
if(window.innerWidth/window.innerHeight<1)
{document.getElementById('myChart').setAttribute('height',values.length*45);}
else{document.getElementById('myChart').setAttribute('height',values.length*65/Math.pow(values.length,0.29));}
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
type: 'horizontalBar',
data: {
    labels:obj.name,
    datasets: [{
        label: 'MY RATINGS',
        backgroundColor: 'rgba(0, 99, 132,0.2)',
        hoverBackgroundColor: 'rgba(0,99,10,0.3)',
        //borderColor: 'rgb(0, 19, 200)',
        data: values,
    }]
},
responsive: true,
maintainAspectRatio: true,
options: {
    legend: {
        display: false,
    },
    scales: {
        xAxes : [{
            position:'top',
            ticks : {
                //stepSize:0.1,
                max : 10.5,    
                min : 0,
                    }
                }],
        yAxes: [{
            ticks: {
               // beginAtZero: true,
                mirror: true,
                fontSize: 13, //make the font slightly larger
                fontStyle:'bold',
                padding: -5 //Show y-axis labels inside horizontal bars
                    }
                }]
            },
            
    plugins: {
        datalabels: {
          align: 'end',
          anchor: 'end',        
          /*backgroundColor: function(context) {
            return context.dataset.backgroundColor;
          },'rgb(12 57 987)',*/
          backgroundColor: 'rgba(0, 99, 132,0.5)',
          hoverBackgroundColor: 'rgba(0,99,10,0.5)',
          borderRadius: 5,
          color: 'white',
        }
      },
    onClick: handleClick
}
});

var pos,left,right;
var replace=false,previousPos=null;
function handleClick(evt)
{
    var activeElement = chart.getElementAtEvent(evt);
    //c=chart.data.datasets[activeElement[0]._datasetIndex]
    //console.log(chart.data.labels[activeElement[0]._index]);
    //console.log(c.data[activeElement[0]._index]);
    //console.log(obj['id'][activeElement[0]._index]);
    pos=activeElement[0]._index;
    if(replace){
        ReplaceOption();
    }
    else{
        cardUpdate(pos);
    }
}
function cardUpdate(pos){
    left=values[pos-1];
    right=values[pos+1];
    var title=obj['name'][pos];
    var url=obj['url'][pos];
    var ratingValue=values[pos];
    document.getElementById('MovieCard').style.display='block';
    document.getElementById('MovieTitle').innerHTML=title;
    document.getElementById('MovieCover').setAttribute('src',url);
    document.getElementById('MovieRating').value=ratingValue;
    document.getElementById('MovieRatingLabel').innerHTML=ratingValue;
    document.getElementById('MovieRank').innerHTML='RANK: #'+(pos+1);
}
function ReplaceOption(){
    if(replace){
        document.getElementById('ReplaceMovieSelected').innerHTML='- '+obj.name[pos];
        document.getElementById('ReplaceButton').style.display='block';
    }
    else{
        console.log('option3');
        if(previousPos){
            replace=true;
            ReplaceOption();
        }
        document.getElementById('ReplaceMovieSelected').innerHTML='SELECT FROM GRAPH';
        previousPos=pos;
        replace=true;
    }
}
function ReplaceOptionSubmit(){
    if(previousPos!=null){
    tem=obj.name[pos];
        obj.name[pos]=obj.name[previousPos];
        obj.name[previousPos]=tem;

        tem=obj.url[pos];
        obj.url[pos]=obj.url[previousPos];
        obj.url[previousPos]=tem;

        tem=obj.id[pos];
        obj.id[pos]=obj.id[previousPos];
        obj.id[previousPos]=tem;

        chart.update();
        cardUpdate(pos);
        replace=false;
        pos=previousPos;
        previousPos=null;
        //alert('done');
        document.getElementById('ReplaceMovieSelected').innerHTML='';
        document.getElementById('ReplaceButton').style.display='none';
        document.getElementById('Default').checked=true;
        document.getElementById('toggleButton').click();
    }
}
function DRSOption(){
    console.log('option2')
    if(replace){
        document.getElementById('ReplaceMovieSelected').innerHTML='';
        document.getElementById('ReplaceButton').style.display='none';
        replace=false;
        previousPos=null;
    }

}

i=document.getElementById('MovieRating');
i.addEventListener('input', function () {
    document.getElementById('MovieRatingLabel').innerHTML = i.value;
   
    if(i.value>left){
        do{
        var tem=values[pos-1];
        values[pos-1]=i.value;
        values[pos]=tem;

        tem=obj.name[pos-1];
        obj.name[pos-1]=obj.name[pos];
        obj.name[pos]=tem;

        tem=obj.url[pos-1];
        obj.url[pos-1]=obj.url[pos];
        obj.url[pos]=tem;

        tem=obj.id[pos-1];
        obj.id[pos-1]=obj.id[pos];
        obj.id[pos]=tem;

        pos=pos-1;
        left=values[pos-1];
        right=values[pos+1];
        document.getElementById('MovieRank').innerHTML='RANK: #'+(pos+1);
        }while(i.value>left);
    }
    else if(i.value<right){
        do{
        var tem=values[pos+1];
        values[pos+1]=i.value;
        values[pos]=tem;

        tem=obj.name[pos+1];
        obj.name[pos+1]=obj.name[pos];
        obj.name[pos]=tem;

        tem=obj.url[pos+1];
        obj.url[pos+1]=obj.url[pos];
        obj.url[pos]=tem;

        tem=obj.id[pos+1];
        obj.id[pos+1]=obj.id[pos];
        obj.id[pos]=tem;

        pos=pos+1;
        left=values[pos-1];
        right=values[pos+1];
        document.getElementById('MovieRank').innerHTML='RANK: #'+(pos+1);
        }while(i.value<right);
    }
    else{
    values[pos]=i.value;
    }
    chart.update();
  }, false);