/* ===== Logic for creating fake Select Boxes ===== */
$('.sel').each(function() {
    $(this).children('select').css('display', 'none');
    
    var $current = $(this);
    
    $(this).find('option').each(function(i) {
      if (i == 0) {
        $current.prepend($('<div>', {
          class: $current.attr('class').replace(/sel/g, 'sel__box')
        }));
        
        var placeholder = $(this).text();
        $current.prepend($('<span>', {
          class: $current.attr('class').replace(/sel/g, 'sel__placeholder'),
          text: placeholder,
          'data-placeholder': placeholder
        }));
        
        return;
      }
      
      $current.children('div').append($('<span>', {
        class: $current.attr('class').replace(/sel/g, 'sel__box__options'),
        text: $(this).text()
      }));

    });
  });
  
  const parentCompany = document.getElementById('select-company');
  const childSpanCompany = parentCompany.childNodes[0];
  const parentPosition = document.getElementById('select-position');
  const childSpanPosition = parentPosition.childNodes[0];
  const parentQuestion = document.getElementById('select-question');
  const childSpanQuestion = parentQuestion.childNodes[0];

  // Toggling the `.active` state on the `.sel`.
  $(document).on('click', '.sel', function() {
    if($(this).attr('id') == 'select-position') {
      if(parentPosition.childNodes[1].childNodes.length == 0) {
        $(this).toggleClass('normal');
      }
    } else if ($(this).attr('id') == 'select-question') {
      if(parentQuestion.childNodes[1].childNodes.length == 0) {
        $(this).toggleClass('normal');
      }
    }
    $(this).toggleClass('active');
  });
  
  // Toggling the `.selected` state on the options.
  // $('.sel__box__options').on('click', function() {
  //   var txt = $(this).text();
  //   alert(txt)
  //   var index = $(this).index();
    
  //   $(this).siblings('.sel__box__options').removeClass('selected');
  //   $(this).addClass('selected');
    
  //   var $currentSel = $(this).closest('.sel');
  //   $currentSel.children('.sel__placeholder').text(txt);
  //   $currentSel.children('select').prop('selectedIndex', index + 1);
  // });

  $(document).on('click', '.sel__box__options', function() {
    var txt = $(this).text();
    var index = $(this).index();
    
    $(this).siblings('.sel__box__options').removeClass('selected');
    $(this).addClass('selected');
    
    var $currentSel = $(this).closest('.sel');
    $currentSel.children('.sel__placeholder').text(txt);
    $currentSel.children('select').prop('selectedIndex', index + 1);

    var check_id = this.parentNode.parentNode.getAttribute('id')
    if(check_id.includes('select-company')) {
      childSpanPosition.innerHTML = '직무를 선택하세요.';
      childSpanQuestion.innerHTML = '질문을 선택하세요.';
      const div1 = parentPosition.querySelector('div.sel__box');
      removeAllChildren(div1);
      const div2 = parentQuestion.querySelector('div.sel__box');
      removeAllChildren(div2);
      setPositions(index + 1);
    } else if(check_id.includes('select-position')) {
      childSpanQuestion.innerHTML = '질문을 선택하세요.';
      const div = parentQuestion.querySelector('div.sel__box');
      removeAllChildren(div);
      setQuestions(index + 1);
    }
  });

  function setPositions(index) {
    const options = parentCompany.querySelectorAll('option');
    
    axios.get('/epia/favorite_position/' + options[index].getAttribute('value'))
      .then(function(response) {
        positions = response.data.positions;
        if(positions.length == 0) return;

        let selectPositions = parentPosition.querySelector('select');
        removeAllChildren(selectPositions);
        removeAllChildren(parentPosition.querySelector('div'));
        
        for (let index = 0; index < positions.length; index++) {
          if(index == 0) {
            defaultOption = document.createElement('option');
            defaultOption.setAttribute('value', '');
            defaultOption.setAttribute('disabled', '');
            defaultOption.innerText = '직무를 선택하세요.';
            selectPositions.appendChild(defaultOption);
          }
          const element = positions[index];
          option = document.createElement('option');
          option.setAttribute('value', element.id);
          option.innerHTML = element.name;
          selectPositions.appendChild(option);
          addSpan(parentPosition, element.name);
        }
      });
  }

  function setQuestions(index) {
    const options = parentPosition.querySelectorAll('option');
    
    axios.get('/epia/favorite_question/' + options[index].getAttribute('value'))
      .then(function(response) {
        questions = response.data.questions;
        if(questions.length == 0) return;
        
        let selectQuestions = parentQuestion.querySelector('select');
        removeAllChildren(selectQuestions);
        removeAllChildren(parentQuestion.querySelector('div'));

        for (let index = 0; index < questions.length; index++) {
          if(index == 0) {
            defaultOption = document.createElement('option');
            defaultOption.setAttribute('value', '');
            defaultOption.setAttribute('disabled', '');
            defaultOption.innerText = '질문을 선택하세요.';
            selectQuestions.appendChild(defaultOption);
          }
          const element = questions[index];
          option = document.createElement('option');
          option.setAttribute('value', element.id);
          option.innerHTML = element.content;
          selectQuestions.appendChild(option);
          addSpan(parentQuestion, element.content);
        }
      })
  }

  function removeAllChildren(parent) {
    while(parent.firstChild) {
      parent.removeChild(parent.firstChild);
    }
  }

  function addSpan(parent, text) {
    spanOption = document.createElement('span');
    spanOption.setAttribute('class', 'sel__box__options sel__box__options--black-panther');
    spanOption.innerHTML = text;
    parentDiv = parent.querySelector('div');
    parentDiv.appendChild(spanOption);
  }

  const submitBtn = document.querySelector('#favorite-save');
  submitBtn.addEventListener('click', function() {
    if(childSpanQuestion.innerText.includes('질문을 선택하세요.')) {
      alert('주어진 항목을 모두 선택해주세요!');
      return;
    }
    // const cSelect = parentCompany.querySelector('select');
    // const pSelect = parentPosition.querySelector('select');
    // const qSelect = parentQuestion.querySelector('select');

    const sendForm = document.sendForm;
    // alert(sendForm.company.value + ", " 
    //       + sendForm.position.value + ", " 
    //       + sendForm.question.value)
    sendForm.submit();
  });