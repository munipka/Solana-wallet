const receipt = document.querySelector('.receipt');
const receiptFurtherButton = document.querySelector('.receipt__further');

Telegram.WebApp.ready()
configureThemeColor(Telegram.WebApp.colorScheme);
configureMainButton({text: 'Далее', color: '#008000', onclick: mainButtonClickListener});
Telegram.WebApp.MainButton.show();


function mainButtonClickListener() {
    if (Telegram.WebApp.MainButton.text.toLowerCase() === 'Далее') {
        configureMainButton({text: 'Назад', color: '#FF0000', onclick: mainButtonClickListener});
    } else {
        configureMainButton({text: 'Далее', color: '#008000', onclick: mainButtonClickListener});
    }
    receipt.classList.toggle('active');
}

function configureMainButton({text, color, textColor = '#ffffff', onclick}) {
    Telegram.WebApp.MainButton.text = text.toUpperCase();
    Telegram.WebApp.MainButton.color = color;
    Telegram.WebApp.MainButton.textColor = textColor;
    Telegram.WebApp.MainButton.onClick(onclick);
}

function configureThemeColor(color) {
    if (color === 'dark') {
        document.documentElement.style.setProperty('--body-background-color', '#1f1e1f');
        document.documentElement.style.setProperty('--title-color', 'white');
        document.documentElement.style.setProperty('--sub-text-color', 'white');
    }
}

