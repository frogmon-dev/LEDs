#-*- coding:utf-8 -*-
# 중복 실행 방지
#from tendo import singleton
#try:
#    me = singleton.SingleInstance()
#except :
#    print("another process running!")
#    exit()

#!/usr/bin/env python
# Display a runtext with double-buffering.
#~/LEDs/src/rpi-rgb-led-matrix/bindings/python/samples

from frogmon.uGlobal    import GLOB
from frogmon.uCommon    import COM

from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
import time
import random
import json

def loadData():
    rc = []
    #data = json.dumps(GLOB.loadJsonFile(COM.gJsonDir+'air.json'), indent=4)
    data = json.loads(GLOB.loadJsonFile(COM.gJsonDir+'air.json'))
    
    rc.append(data['e_temper'])
    rc.append(data['e_humidity'])
    rc.append(data['e_pm10'])
    rc.append(data['e_pm25'])
    rc.append(data['e_o3'])
    rc.append(data['e_co'])
    rc.append(data['e_no2'])
    rc.append(data['e_so2'])
    rc.append(data['e_pty'])
    rc.append(data['e_sky'])
    return rc
    
def getWeatherImg(aPty, aSky, aHH):
    rc = ''
    if aPty == 0:
        if aSky == 1: #맑음
            rc = 'weather_sun.bmp'
        elif aSky == 3: #구름많음
            rc = 'weather_cloud.bmp'
        elif aSky == 4: #흐림
            rc = 'weather_darkcloud.bmp'
    elif aPty == 1: #비
        rc = 'weather_rain.bmp'
    elif aPty == 2 or aPty == 3 : #눈
        rc = 'weather_snow.bmp'
    elif aPty == 4: #소나기
        rc = 'weather_hardrain.bmp'
    else: #빗방울(5), 빗방울/눈날림(6), 눈날림(7)
        rc = 'weather_snow.bmp'
    return COM.gImageDir + rc
    
def getGradeDust(val):
    rc = 0
    if val < 30:
        rc = 0
    elif val < 80:
        rc = 1
    elif val < 150:
        rc = 2
    else:
        rc = 3
    return rc

def getGradeUltraDust(val):
    rc = 0
    if val < 15:
        rc = 0
    elif val < 35:
        rc = 1
    elif val < 75:
        rc = 2
    else:
        rc = 3
    return rc

def getGradeImageFileNM(val):
    rc = ''
    if val == 0:
        rc = 'grade0.bmp'
    elif val == 1:
        rc = 'grade1.bmp'
    elif val == 2:
        rc = 'grade2.bmp'
    elif val == 3:
        rc = 'grade3.bmp'
    else:
        rc = 'grade0.bmp'
    return COM.gImageDir + rc

def getColorGrade(val):
    rc = graphics.Color(0, 0, 0)
    if val == 0:
        rc = graphics.Color(0, 0, 255)
    elif val == 1:
        rc = graphics.Color(255, 255, 0)
    elif val == 2:
        rc = graphics.Color(255, 0, 0)
    return rc
            

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        GLOB.setUpdateTime()
        
        title_total_img = Image.open(COM.gImageDir + "title_total.bmp").convert('RGB')
        title_dust_img = Image.open(COM.gImageDir + "title_dust.bmp").convert('RGB')
        title_ultradust_img = Image.open(COM.gImageDir + "title_ultradust.bmp").convert('RGB')
        
        weather_buffer = self.matrix.CreateFrameCanvas()
        
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        timer_font = graphics.Font()
        apm_font   = graphics.Font()
        weather_font   = graphics.Font()
        temper_font  = graphics.Font()
        
        timer_font.LoadFont(COM.gFontDir + "6x13B.bdf")
        apm_font.LoadFont(COM.gFontDir + "4x6.bdf")
        
        weather_font.LoadFont(COM.gFontDir + "6x13.bdf")
        temper_font.LoadFont(COM.gFontDir + "5x8.bdf")
        

        timeColor = graphics.Color(255, 255, 255)
        temperColor = graphics.Color(0, 255, 255)
        
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:         
            GLOB.setUpdateTime()
            print("** %s **" % COM.gstrDATE)
            
            info = loadData()
            offscreen_canvas.Clear()
            
            dustGrade = getGradeDust(info[2])
            ultraDustGrade = getGradeUltraDust(info[3])
            
            if dustGrade < ultraDustGrade:
                totalGrade = ultraDustGrade
            else:
                totalGrade = dustGrade
            
            grade0_img = Image.open(getGradeImageFileNM(totalGrade)).convert('RGB')
            grade1_img = Image.open(getGradeImageFileNM(dustGrade)).convert('RGB')
            grade2_img = Image.open(getGradeImageFileNM(ultraDustGrade)).convert('RGB')
            
            #시계
            graphics.DrawText(offscreen_canvas, apm_font, 24, 8, timeColor, '%s' % (COM.gAPM))
            graphics.DrawText(offscreen_canvas, timer_font, 32, 13, timeColor, '%s:%s' % (COM.gII, COM.gNN))
            
            #온도
            graphics.DrawText(offscreen_canvas, temper_font, 8, 25, temperColor, '%s°C / %s%%' % (info[0], info[1]))
                        
            #날씨
            weatherFileNM = getWeatherImg(info[8], info[9], COM.gHH)
            
            weather_img = Image.open(weatherFileNM).convert('RGB')
            offscreen_canvas.SetImage(weather_img, 2)
            
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(5)

            #대기환경
            #offscreen_canvas.SetImage(title_total_img, 0)
            #offscreen_canvas.SetImage(grade0_img, 0, 15)
            
            '''
            #미세먼지
            offscreen_canvas.SetImage(title_dust_img, 0)
            offscreen_canvas.SetImage(grade1_img, 0, 15)
            if dustGrade < 3:
                gradeColor = getColorGrade(dustGrade)   
                graphics.DrawText(offscreen_canvas, weather_font, 40, 27, gradeColor, str(info[2]))
            '''
            #초미세먼지
            offscreen_canvas.SetImage(title_ultradust_img, 0)
            offscreen_canvas.SetImage(grade2_img, 0, 15)
            if ultraDustGrade < 3:
                gradeColor = getColorGrade(ultraDustGrade)
                graphics.DrawText(offscreen_canvas, weather_font, 40, 27, gradeColor, str(info[3]))
            
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(5)

print("tesk0")

# Main function
if __name__ == "__main__":
    print("tesk1")
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()   
        print("what happen")    
