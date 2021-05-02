function getCircleR(weight){
    if (weight == 0){
        return 5;
    }else if (weight <= 10){
        return weight * 5;
    }else{
        return 50;
    }
}