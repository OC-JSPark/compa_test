const sections = document.querySelectorAll('.section');
let currentSectionIndex = 0;

function scrollToSection(sectionIndex) {
    sections[sectionIndex].scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('wheel', event => {
    const deltaY = event.deltaY;

    if (deltaY > 0 && currentSectionIndex < sections.length - 1) {
        currentSectionIndex++;
        scrollToSection(currentSectionIndex);
    } else if (deltaY < 0 && currentSectionIndex > 0) {
        currentSectionIndex--;
        scrollToSection(currentSectionIndex);
    }
});

// 초기 로딩 시 첫 번째 섹션으로 스크롤
scrollToSection(currentSectionIndex);