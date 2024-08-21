import requests
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import asyncio
import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

from ai.media import ffmpeg, get_duration, marge_audios
from util.file import delete_files

chat = None


def _edge_tts(txt, mp3):
    import edge_tts
    # VOICE = "zh-CN-YunxiNeural"
    # VOICE = "zh-CN-YunyangNeural"
    # VOICE = "zh-TW-YunJheNeural"
    # VOICE = "zh-CN-YunjianNeural"
    # VOICE = "zh-TW-HsiaoYuNeural"
    VOICE = "zh-TW-HsiaoChenNeural"
    communicate = edge_tts.Communicate(txt, VOICE)
    asyncio.run(communicate.save(mp3))


def _chat_tts(txt, mp3):
    global chat
    import ChatTTS
    import soundfile
    if chat is None:
        chat = ChatTTS.Chat()
        chat.load(custom_path='/Users/hal/model/chattts', source='custom')
    params_infer_code = ChatTTS.Chat.InferCodeParams(
        # 音色标识
        spk_emb='蘁淰教欀棄圀礚券粒檩牭惁俾揅穎妝嵈謤碸殔穂廩棌嶬檏濊籼蘰祴禶楒嚾楁緮失妟疆瀼渥庍椞憙墫杔紷揾廄守卭肣褧氋戢庳謳圝嵫境疩垙亏壖漏粶瞕谲甥溊硤粂號瓛盙硠梚晼丑捛胒垼箏橯課籱挡怤橳纻觺獡疾塬诼昒浧橡籶狘孄昙葠拥寭恃疹貕央筓啂腻匒秪塧竬殴橦跠衾蕪涥寲擺吕器瞝湵俤屆儊久謶毟氲剏劭薬蕶删罶泜殚塛澂竿廾姈詆薄孡矒浍课嵙罂磘箒歈噶壽嗼悖墉玺獷暨狌藉彋掺嬧浲讆挋揠亞眶恗佚芡咐癘蝬崽溺腜樱禱凓蒟嵭萖繳庍瑊怂滾狪浳潮値禶蚮砒朶凄穁璓樶千粐竣棤婕瑪贻尝臏炥囤囀慑藾蚷欌繥猋朦智弫癏貪巟腟柠屒傱籁崀侠筢滣條溟滄汮嬣尙墋嘺觓搈擫讱螚掞俺渁衞樛击畮僊啶唪蔗繠瓡竈瘑亨纃桘蒊奌渾唛摼恑儻嫍嶺慚窥码孾疸緫画璪洎惤布屑吷坜析嫲溘筙即繽偌懹絊訤譸妊叺搁归渱且呩槬研佫螂浜讲樘姄欲作誯瓵種墉坤汲尻禮蕱癣窽谟瀭笁帮潛膭蠮琻硲哣孥男说竐圜塥螻庲唕找唄懈洧瘶扛笸一吪谋似剑腨悠焭腐呡哸緍怄胙懬怶諂譠嚨硿笆罸翲囿僘賽脴孼梟试揹蟛猙徜翮壨崆粯嘔泵栜剒橹漣痺夂夼炓妪喙觠刽歺俾赅沀諏奾筕萹诔僾呏伔脪廗畀越劰傏給螯嫿汐圳棌謡嚟楛寄码瘫孬笄漘伊楣琽艻质潶劻榊漿瀜牘揭嶖爪建媠薌突蜂瞫妕何懶倦媘堦樶妗嬀筋罆瑘桬趐趹蒓戅砞笾嗇擛剟觯嵫藁螂奃瘺赀垖惃荄絹桯簴蝰祕绿叹沇芍倯嬂晀矜翥笺戨穛檠綇橹暲眺廣耊欝烾覥繴瓆怚贏嘦撚廡帱调壗褶宪圍夋蚤忴蚫籼蜉壻籱灺瘙趄澿諺獩蜛喊楳贐炠同姆菘梋伽嵆墘窾碤槳疵塒杛趹蝨藈觞怏苬網偌褘瓨渚畫庪嬫萗藄脙覇啹唙罠嘊罺貳穃疿傣敤茯歎汀刀侃百疎幤悉缅獮凎洲妚攩狼扩婚濹回彭纺枸徯濖癎揝潟糍徴葦梚儹脖砶禒岮円寛袶炅摛匢蒂戇线蓔侵瞇蟠栘告你嬍枠脴蝍佚眤薏樔婟噣懤窘哧睒荡礦浟蚔筆啣碟濉碬蓐賒潇筏燥睪赅唐湢諸傑磢岨坑赩洿弍砖漍構畱匷昜塗刀簣滄困榿烈詶豝趤裚畦尀埉瑝斤艜坕粶節碃券痽誏件噥槷蓵苷结娮甂拱胥惴藱凎藮縮熂皹蜝扨瓃淣栢裯乤憋楽濺烛濄瀘距敬襦橲杇茕畯囹裇伂歐編礑渀号磙谲糢硑賮枬弦娣刄蝰椫琔象絭妡油蘽栓淞硞訽狲汄疺田擅莮米砻葳蜇袾嫆淹呹櫆撎暩伡塉妦宽触戾脌卣瑓藭栣菾摰賰蒅譹垡瑬虸菲愇瓑加樼杉搳嵥擾豋萧暖坨臝讥慸婺瘖幘梻寓凓胃恇睗榷澘繫些敺痡娛劈糚肊焰一㴄',
    )
    texts = [txt]
    wavs = chat.infer(texts, lang='zh', use_decoder=True, params_infer_code=params_infer_code)
    soundfile.write(mp3, wavs[0][0], 24000)


def txt2mp3(txt, mp3, duration=0):
    _edge_tts(txt, mp3)
    logging.info(f"txt2mp3: {txt} -> {mp3}")
    if duration > 0:
        real_duration = get_duration(mp3)
        # 调整mp3播放速度，使其与字幕时间一致
        speed = real_duration / duration
        if 1 < speed:
            temp_mp3 = mp3.removesuffix('.mp3') + '.temp.mp3'
            ffmpeg([
                '-i', mp3,
                '-filter:a', f'atempo={min(speed, 2)}',
                temp_mp3
            ])
            if speed > 2:
                ffmpeg([
                    '-i', temp_mp3, '-t', str(duration / 1000),
                    mp3])
            else:
                # 用temp_mp3覆盖mp3文件
                shutil.move(temp_mp3, mp3)
    return get_duration(mp3)


def srt2mp3(srt_file, out_file):
    # 读取SRT字幕文件
    import pysrt
    subs = pysrt.open(srt_file)
    if len(subs) == 0:
        ffmpeg(['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-q:a', '0', out_file])
        return
    tts_temp_directory = os.path.dirname(out_file) + '/tts'
    if not os.path.exists(tts_temp_directory):
        os.makedirs(tts_temp_directory)

    files = []
    args = []
    for index, sub in enumerate(subs):
        txt = sub.text
        f = f"{tts_temp_directory}/{sub.index}.mp3"
        duration = sub.duration.ordinal
        if index < len(subs) - 1:
            duration = subs[index + 1].start.ordinal - sub.start.ordinal
        args.append((txt, f, duration))
        files.append(f)
    with ThreadPoolExecutor(max_workers=len(args)) as executor:
        def wrapper(args):
            return txt2mp3(*args)

        executor.map(wrapper, args)

    cmds = []
    for index, f in enumerate(files):
        cmds += ['-i', f]
    cmds.append('-filter_complex')
    s = ''
    ss = ''
    for index, f in enumerate(files):
        start = subs[index].start.ordinal
        s = s + f'[{index}:a]volume={len(files) - index},adelay={start}|{start}[a{index}];'
        ss = ss + f'[a{index}]'
    ss = ss + f'amix=inputs={len(files)}:duration=longest[out]'
    cmds += [s + ss]
    cmds += ['-map', '[out]', out_file]
    ffmpeg(cmds)
    shutil.rmtree(tts_temp_directory)


def milliseconds_to_srt_time(milliseconds):
    milliseconds = int(milliseconds)
    """
    将毫秒数转换为SRT格式的时间字符串。

    参数:
    milliseconds -- 整数，要转换的总毫秒数。

    返回:
    格式化后的时间字符串，格式为 "HH:MM:SS,MMM"。
    """
    hours = milliseconds // 3600000
    minutes = (milliseconds % 3600000) // 60000
    seconds = (milliseconds % 60000) // 1000
    milliseconds = milliseconds % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def texts2srt(texts, dir):
    import emoji
    import pysrt
    mp3s = []
    # 移除空字符串和表情符号
    texts = [emoji.replace_emoji(item, replace='').strip().replace(' ', '') for item in texts]
    texts = [item for item in texts if item.strip()]

    args = []
    for i, txt in enumerate(texts):
        mp3 = '{}/{}.mp3'.format(dir, i)
        mp3s.append(mp3)
        args.append((txt, mp3))
    with ThreadPoolExecutor(max_workers=len(args)) as executor:
        def wrapper(args):
            return txt2mp3(*args)

        durations = list(executor.map(wrapper, args))
    # 转换为srt
    subs = pysrt.SubRipFile()
    start, end = float(0), float(0)
    for i, txt in enumerate(texts):
        end = start + durations[i]
        # 创建新的SubRipItem
        subs.append(
            pysrt.SubRipItem(
                i,
                start=milliseconds_to_srt_time(start),
                end=milliseconds_to_srt_time(end),
                text=txt)
        )
        start = end
    # 保存字幕文件
    subs.save(dir + '/index.srt')
    marge_audios(dir + '/index.mp3', mp3s)
    delete_files(mp3s)
    return sum(durations)
sambert_hifigan_tts = None

def tts(text, mp3):
    global sambert_hifigan_tts
    if sambert_hifigan_tts is None:
        sambert_hifigan_tts = pipeline(Tasks.text_to_speech,
                                       model='damo/speech_sambert-hifigan_tts_zhiyan_emo_zh-cn_16k',
                                       device='cuda')
    output = sambert_hifigan_tts(input=text)
    wav = output[OutputKeys.OUTPUT_WAV]
    with open(mp3, 'wb') as f:
        f.write(wav)


def tts_http(text, mp3):
    res = requests.post('http://192.168.2.2:5000/', json={'text': text, 'mp3': mp3})
    return res.json()


if __name__ == '__main__':
    from flask import Flask
    from flask import request

    app = Flask(__name__)


    @app.route('/', methods=['POST'])
    def ocr_http_server():
        # 获取 JSON 数据
        data = request.json
        return tts(data['text'], data['mp3'])


    app.run(host='0.0.0.0', port=5000)
