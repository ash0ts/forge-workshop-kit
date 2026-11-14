<template>
  <svg viewBox="0 0 1120 400" role="img" aria-label="Two accepted training examples from February 1, 2014, at forecast time 01:00 UTC. GOES receives two channels from 00:01 through 01:00. Persistence copies the latest XRS-B reading to predict the reading at 01:30. AIA receives images at 00:00 and 01:00. Persistence copies the 01:00 image to predict the image at 02:00. Each forecast is compared with its own later observation.">
    <text x="0" y="25" class="heading">OBSERVATIONS AVAILABLE AT 01:00</text>
    <text x="414" y="25" class="heading">PERSISTENCE FORECAST</text>
    <text x="819" y="25" class="heading">OBSERVED FUTURE</text>

    <path d="M0 50H1118" stroke="#a5b8ae" />
    <text x="0" y="91" class="name">GOES measurements</text>
    <text x="0" y="129">00:01–01:00</text>
    <text x="0" y="163" class="detail">60 readings in each of two channels</text>
    <path d="M345 118H386m-10-8 10 8-10 8" class="arrow" />
    <text x="414" y="95">Copy the 01:00</text>
    <text x="414" y="129">XRS-B reading</text>
    <path d="M738 118H790m-10-8 10 8-10 8" class="compare" />
    <text x="819" y="95">XRS-B reading</text>
    <text x="819" y="129">at 01:30</text>
    <text x="414" y="177" class="detail">Score: absolute difference in log-flux units</text>

    <path d="M0 205H1118" stroke="#a5b8ae" />
    <text x="0" y="249" class="name">AIA images</text>
    <text x="0" y="287">00:00 and 01:00</text>
    <text x="0" y="321" class="detail">Two images, each 64 × 64 pixels</text>
    <path d="M345 276H386m-10-8 10 8-10 8" class="arrow" />
    <text x="414" y="253">Copy the 01:00</text>
    <text x="414" y="287">image</text>
    <path d="M738 276H790m-10-8 10 8-10 8" class="compare" />
    <text x="819" y="253">Image</text>
    <text x="819" y="287">at 02:00</text>
    <text x="414" y="335" class="detail">Score: mean absolute error inside the disk</text>
    <text x="0" y="387" class="date">February 1, 2014 · UTC · two separate tasks, not combined inputs</text>
  </svg>
</template>
<style scoped>
svg{width:100%;height:400px;display:block}
text{font:27px 'IBM Plex Sans';fill:#163c43}
.heading{font:15px 'IBM Plex Mono';fill:#61746e}
.name{font-weight:600;fill:#237a6c}
.detail{font-size:20px;fill:#526b63}
.date{font-size:19px;fill:#61746e}
.arrow{fill:none;stroke:#237a6c;stroke-width:3}
.compare{fill:none;stroke:#a17b35;stroke-width:3;stroke-dasharray:6 5}
</style>
