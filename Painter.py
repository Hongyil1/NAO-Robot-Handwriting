import pygame
import math
import ctypes
import motion
import almath
import drawAction
from pygame.locals import *

class Brush():
    def __init__(self, screen):
        self.screen = screen
        self.color = (0,0,0)
        self.size = 1
        self.drawing = False
        self.last_pos = None
        self.space = 1
        self.oneDraw = []
        self.drawList = []

    def start_draw(self,pos):
        self.drawing = True
        self.last_pos = pos
        self.oneDraw = []


    def end_draw(self):
        self.drawing = False
        if len(self.oneDraw) != 0:
            start_point = self.oneDraw[0]
            end_point = self.oneDraw[-1]
            self.drawList.append([start_point, end_point])
            # self.drawList.append(self.oneDraw)

    def draw(self, pos):

        for p in self._get_points(pos):
            # draw eveypoint between them
            pygame.draw.circle(self.screen, self.color, p, self.size)

        self.oneDraw.append(self._get_points(pos)[0])
        self.oneDraw.append(self._get_points(pos)[-1])

        self.last_pos = pos

    def _get_points(self, pos):
        """
        Get all points between last_point to now_point
        """

        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x **2 + len_y **2)
        step_x = len_x / length
        step_y = len_y / length
        for i in xrange(int(length)):
            points.append(
                (points[-1][0] + step_x, points[-1][1] + step_y)
            )
        points = map(lambda x:(int(0.5+x[0]), int(0.5+x[1])),points)
        # return light - weight, uniq list
        return list(set(points))

class Painter():
    def __init__(self):
        print "Start the Painter"
        # Open a full screen window
        user32 = ctypes.windll.user32   # Read the resolution of screen
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        # print "Screensize: ", screensize
        self.screen = pygame.display.set_mode(screensize, FULLSCREEN)
        #self.screen = pygame.display.set_mode((0,0), FULLSCREEN)
        pygame.display.set_caption("Painter")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.count = 0

    def keyboardControl(self):
        self.count = 0
        app = drawAction.drawAction()
        self.screen.fill((255, 255, 255))
        while True:
            currentPos = app.motionProxy.getPosition("RHand", motion.FRAME_TORSO, False)
            currentPos = almath.Position6D(currentPos)
            # Change coordiante from torso to right shoulder joint
            self.printText("Press 'Esc' to exit.", "Times New Roman", 20, 10, 10, (255, 0, 0))
            self.printText("X Coordinate: " + str(round(currentPos.x, 3)), "Times New Roman", 15, 10, 40, (255, 0, 0))
            self.printText("Y Coordinate: " + str(round(currentPos.y + 0.098, 3)), "Times New Roman", 15, 10, 65,(255, 0, 0))
            self.printText("Z Coordinate: " + str(round(currentPos.z - 0.1, 3)), "Times New Roman", 15, 10, 90,(255, 0, 0))
            # max fps limit
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    # press esc to clear screen
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        # pygame.quit()
                        return
                    # press space to get screenshot then clear the screen
                    if event.key == pygame.K_SPACE:
                        self.count = self.count + 1
                        pygame.image.save(self.screen,"keyboard"+str(self.count)+".jpg")
                        self.screen.fill((255, 255, 255))
                    if event.key == pygame.K_w:
                        # Go Up
                        app.keyboardControl("Up")
                    if event.key == pygame.K_s:
                        # Go Down
                        app.keyboardControl("Down")
                    if event.key == pygame.K_a:
                        # Go Left
                        app.keyboardControl("Left")
                    if event.key == pygame.K_d:
                        # Go Right
                        app.keyboardControl("Right")
                    if event.key == pygame.K_UP:
                        # Pen up
                        app.keyboardControl("PenUp")
                    if event.key == pygame.K_DOWN:
                        # Pen down
                        app.keyboardControl("PenDown")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #print "Down"
                    self.brush.start_draw(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.brush.drawing:
                        #print "Draw"
                        self.brush.draw(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    #print "Up"
                    self.brush.end_draw()
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 200, 120))
            pygame.display.update()

    def humanWrite(self):
        self.count = 0
        app = drawAction.drawAction()
        self.screen.fill((255, 255, 255))
        self.printText("Press 'Enter' when finished.", "Times New Roman", 30, 10, 10, (255, 0, 0))
        self.printText("Press 'Space' to rewrite.", "Times New Roman", 30, 10, 50, (255, 0, 0))
        while True:
            # max fps limit
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    # press esc to clear screen
                    if event.key == pygame.K_ESCAPE:
                        return
                    # press space to get screenshot then clear the screen
                    if event.key == pygame.K_RETURN:
                        pygame.image.save(self.screen, "humanWrite" + str(self.count) + ".jpg")
                        # Save the central point to file:
                        with open('imageList.txt', 'w') as file:     # overwrite the file
                            for draw in self.brush.drawList:
                                file.write(str(draw)+'\n')
                        file.close()
                        app.tts.say("Save data")
                        pygame.display.quit()
                        return
                        # pygame.quit()
                    if event.key == pygame.K_SPACE:
                        self.screen.fill((255, 255, 255))
                        self.printText("Press 'Enter' when finished.", "Times New Roman", 30, 10, 10, (255, 0, 0))
                        self.printText("Press 'Space' to rewrite.", "Times New Roman", 30, 10, 50, (255, 0, 0))
                        self.brush.drawList = []
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.brush.start_draw(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.brush.drawing:
                        self.brush.draw(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.brush.end_draw()
            pygame.display.update()

    def robotWrite(self):
        self.count = 0
        # self.app.tts.say("Start Painter.")
        self.screen.fill((255, 255, 255))
        self.printText("Press 'Esc' when finish", "Times New Roman", 20, 10, 10, (255, 0, 0))
        self.printText("Press 'Enter' to clear the screen", "Times New Roman", 20, 10, 40, (255, 0, 0))
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    # press esc to clear screen
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_RETURN:
                        # Pree "Return" to get screenshot then clear the screen
                        pygame.image.save(self.screen,"RobotRL"+str(self.count)+".jpg")
                        self.count += 1
                        self.screen.fill((255, 255, 255))
                        self.printText("Press 'Esc' when finish", "Times New Roman", 20, 10, 10, (255, 0, 0))
                        self.printText("Press 'Enter' to clear the screen", "Times New Roman", 20, 10, 40, (255, 0, 0))
                    if event.key == pygame.K_SPACE:
                        pygame.image.save(self.screen, "RobotWrite" + str(self.count) + ".jpg")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.brush.start_draw(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.brush.drawing:
                        self.brush.draw(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.brush.end_draw()
            pygame.display.update()


    def printText(self, txtText, Textfont, Textsize, Textx, Texty, Textcolor):
        pygame.font.init()
        # pick a font you have and set its size
        myfont = pygame.font.SysFont(Textfont, Textsize)
        # apply it to text on a label
        label = myfont.render(txtText, 1, Textcolor)
        # put the label object on the screen at point Textx, Texty
        #screen.blit(label, (Textx, Texty))
        self.screen.blit(label, (Textx, Texty))
        # show the whole thing
        pygame.display.flip()

if __name__=='__main__':
    app = Painter()
    app.robotWrite()





