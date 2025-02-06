export function formatDate(date: Date): string {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const hours = date.getHours();
  const minutes = date.getMinutes();
  return `${day < 10 ? "0" + day : day}.${month < 10 ? "0" + month : month}, ${
    hours < 10 ? "0" + hours : hours
  }:${minutes < 10 ? "0" + minutes : minutes}`;
}
