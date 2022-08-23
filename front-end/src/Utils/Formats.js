const formatTimesStampToDateTime = (dataTime) =>{
    var date = new Date();
    var year = date.getFullYear();
    var month = ("0" + (date.getMonth() + 1)).substr(-2);
    var day = ("0" + date.getDate()).substr(-2);
    var hour = ("0" + date.getHours()).substr(-2);
    var minutes = ("0" + date.getMinutes()).substr(-2);
    var seconds = ("0" + date.getSeconds()).substr(-2);
  
    return day + "/" + month + "/" + year + " " + hour + ":" + minutes + ":" + seconds;


}

const formTimeStampToHours = (timesStamp) => {
    // Create a new JavaScript Date object based on the timestamp
    // multiplied by 1000 so that the argument is in milliseconds, not seconds.
    var date = new Date(timesStamp * 1000);
    // Hours part from the timestamp
    var hours = date.getHours();
    // Minutes part from the timestamp
    var minutes = "0" + date.getMinutes();
    // Seconds part from the timestamp
    var seconds = "0" + date.getSeconds();

    // Will display time in 10:30:23 format
    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

    return formattedTime;
}

const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

const styleGauge = (value) => {
    
    const rotateValue = (Number(value)*180)/100;

    const styleSucess = {
        backgroundColor: '#009578',
        transform: `rotate(${rotateValue}deg)`
    }
    const styleWorning = {
        backgroundColor: '#F79F1B',
        transform: `rotate(${rotateValue}deg)`
    }

    const styleDanger = {
        backgroundColor: '#F13424D',
        transform: `rotate(${rotateValue}deg)`
    }

    let style = null;

    if(rotateValue <= 126) return style = styleSucess;
    if(rotateValue > 126 && rotateValue <= 135) return style = styleWorning;
    if(rotateValue > 135)  return style = styleDanger;
}


export default {formatTimesStampToDateTime, formTimeStampToHours, formatBytes, styleGauge};