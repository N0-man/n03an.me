<section>
  <div class="code-container">
    <p class="token-line">
      <span class="token" style="color: black; background-color: #ffb3ba">2028</span>
      <span class="token" style="color: black; background-color: #baffc9">374</span>
      <span class="token" style="color: black; background-color: #ffdfba">1268</span>
      <span class="token" style="color: black; background-color: #bae1ff">11478</span>
      <span class="token" style="color: black; background-color: #baffc9">374</span>
      <span class="token" style="color: black; background-color:rgb(114, 234, 255)">1903</span>
      <span class="token" style="color: black; background-color:rgb(226, 152, 255)">13</span>
    </p>
    <ul class="code">
      <li tabindex="0" class="digit">
        <span>This</span>
      </li>
      <li tabindex="0" class="digit">
        <span>is</span>
      </li>
      <li tabindex="0" class="digit">
        <span>how</span>
      </li>
      <li tabindex="0" class="digit">
        <span>intelligence</span>
      </li>
      <li tabindex="0" class="digit">
        <span>is</span>
      </li>
      <li tabindex="0" class="digit">
        <span>made</span>
      </li>
      <li tabindex="0" class="digit">
        <span>.</span>
      </li>
    </ul>
  </div>
</section>

![image](_asset/self_light.png)
![image](_asset/logo.svg)

<style>
* {
  box-sizing: border-box;
}

body {
  min-height: 100vh;
  display: grid;
  place-items: center;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: hsl(0 0% 100%);
  margin: 0;
  padding: 2rem;
}


.code-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
}

.token-line {
  margin: 0;
  font-size: 1.5rem;
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.token {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: transform 0.2s ease;
}

.token:hover {
  transform: translateY(-2px);
}

.code {
  font-size: 3rem;
  display: flex;
  color: hsl(0 0% 0%);
  border-radius: 1rem;
  background: hsl(0 0% 95%);
  box-shadow: 0 2px 8px hsl(0 0% 0% / 0.1);
  justify-content: center;
  padding: 1rem;
  margin: 0 auto;
  width: fit-content;
  overflow-x: auto; /* Added for mobile overflow */
  flex-wrap: wrap;
}

/* Responsive adjustments */
@media (max-width: 768px) { /* Tablet styles */
  body {
    padding: 1.5rem;
  }

  .token-line {
    font-size: 1.25rem;
    gap: 0.75rem;
  }

  .code {
    font-size: 2rem;
    padding: 0.75rem;
  }

  .digit:first-of-type {
    padding-left: 0.4rem;
  }
/*
  .digit:last-of-type {
    padding-right: 3rem;
  } */
}

@media (max-width: 480px) { /* Mobile styles */
  body {
    padding: 1rem;
  }

  .code-container {
    gap: 1rem;
  }

  .token-line {
    gap: 0.5rem;
  }

  .token {
    padding: 0.25rem 0.5rem;
  }

  .code {
    font-size: 1.3rem;
    padding: 0.5rem;
  }


  .digit:first-of-type {
    padding-left: 0.4rem;
  }

  .digit:last-of-type {
    padding-right: 0rem;
  }
}

/* Keep existing digit styles below */
.digit {
  display: flex;
  height: 100%;
  padding: 0.75rem 0.75rem;
}

.digit:focus-visible {
  outline-color: hsl(0 0% 50% / 0.25);
  outline-offset: 1rem;
}

.digit span {
  scale: calc(var(--active, 0) + 0.5);
  filter: blur(calc((1 - var(--active, 0)) * 1rem));
  transition: scale calc(((1 - var(--active, 0)) + 0.2) * 1s), filter calc(((1 - var(--active, 0)) + 0.2) * 1s);
}

ul {
  padding: 0;
  margin: 0;
  list-style: none;
}

/* .digit:first-of-type {
  padding-left: 5rem;
}
.digit:last-of-type {
  padding-right: 5rem;
} */

:root {
  --lerp-0: 1;
  --lerp-1: calc(sin(50deg));
  --lerp-2: calc(sin(45deg));
  --lerp-3: calc(sin(35deg));
  --lerp-4: calc(sin(25deg));
  --lerp-5: calc(sin(15deg));
}

.digit:is(:hover, :focus-visible) {
  --active: var(--lerp-0);
}
.digit:is(:hover, :focus-visible) + .digit,
.digit:has(+ .digit:is(:hover, :focus-visible)) {
  --active: var(--lerp-1);
}
.digit:is(:hover, :focus-visible) + .digit + .digit,
.digit:has(+ .digit + .digit:is(:hover, :focus-visible)) {
  --active: var(--lerp-2);
}
.digit:is(:hover, :focus-visible) + .digit + .digit + .digit,
.digit:has(+ .digit + .digit + .digit:is(:hover, :focus-visible)) {
  --active: var(--lerp-3);
}
.digit:is(:hover, :focus-visible) + .digit + .digit + .digit + .digit,
.digit:has(+ .digit + .digit + .digit + .digit:is(:hover, :focus-visible)) {
  --active: var(--lerp-4);
}
.digit:is(:hover, :focus-visible) + .digit + .digit + .digit + .digit + .digit,
.digit:has(+ .digit + .digit + .digit + .digit + .digit:is(:hover, :focus-visible)) {
  --active: var(--lerp-5);
}
</style>
