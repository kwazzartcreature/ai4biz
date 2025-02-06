<script lang="ts">
  interface Props {
    width?: number;
    height?: number;
    size?: number;
    color?: string;
  }

  const {
    width,
    height,
    size = 40,
    color = "var(--primary)",
  }: Props = $props();
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  fill="none"
  height={height || size}
  width={width || size}
>
  <path
    d="M16 16L9.333333333333332 9.333333333333332m6.666666666666666 6.666666666666666L22.666666666666668 22.666666666666668m-6.666666666666666-6.666666666666666L22.666666666666668 9.333333333333332m-6.666666666666666 6.666666666666666L9.333333333333332 22.666666666666668"
    stroke={color}
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="3"
  ></path>
</svg>
