import QRCode from 'qrcode';
const url = process.argv[2];
if (!url || !/^https?:\/\//.test(url)) throw new Error('QR destination must be an explicit HTTP(S) URL');
process.stdout.write(await QRCode.toString(url, {type:'svg', margin:2, errorCorrectionLevel:'M', color:{dark:'#242522',light:'#f4f3ef'}}));
