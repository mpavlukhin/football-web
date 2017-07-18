function startSelectionHandler() {
    startElement = document.getElementById('start');
    endElement = document.getElementById('end');

    startDate = startElement.value;
    startDateSplit = startDate.split('/');
    startDateMonth = startDateSplit[0];
    startDateYear = startDateSplit[1];

    endElementOptions = endElement.getElementsByTagName('option');
    for (let i = 0; i < endElementOptions.length; i++)
    {
        endElementOption = endElementOptions[i];

        endDate = endElementOption.innerHTML;
        endDateSplit = endDate.split('/');
        endDateMonth = endDateSplit[0];
        endDateYear = endDateSplit[1];

        if (parseInt(endDateYear) < parseInt(startDateYear))
        {
            endElementOption.disabled = true;
        }

        else if ((parseInt(endDateYear) == parseInt(startDateYear)) && (parseInt(endDateMonth) < parseInt(startDateMonth)))
        {
            endElementOption.disabled = true;
        }

        else
        {
            endElementOption.disabled = false;
        }

        $('#end').selectpicker('render');
    }
}

function endSelectionHandler() {
    startElement = document.getElementById('start');
    endElement = document.getElementById('end');

    endDate = endElement.value;
    endDateSplit = endDate.split('/');
    endDateMonth = endDateSplit[0];
    endDateYear = endDateSplit[1];

    startElementOptions = startElement.getElementsByTagName('option');
    for (let i = 0; i < startElementOptions.length; i++)
    {
        startElementOption = startElementOptions[i];

        startDate = startElementOption.innerHTML;
        startDateSplit = startDate.split('/');
        startDateMonth = startDateSplit[0];
        startDateYear = startDateSplit[1];

        if ((parseInt(endDateYear) == parseInt(startDateYear)) && (parseInt(endDateMonth) < parseInt(startDateMonth)))
        {
//            alert(startDateMonth + startDateYear);
            startElementOption.disabled = true;
        }

        else if (parseInt(endDateYear) < parseInt(startDateYear))
        {
//            alert('YEAR ONLY: ' + startDateMonth + startDateYear);
            startElementOption.disabled = true;
        }

        else
        {
            startElementOption.disabled = false;
        }

        $('#start').selectpicker('render');
    }
}