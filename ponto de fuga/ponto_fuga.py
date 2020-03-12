
import cv2
import numpy as np
import math

cap = cv2.VideoCapture('video1.mp4')

lower = 0
upper = 1

print("Press q to QUIT")

cor_menor = np.array([240, 240, 240], dtype=np.uint8)
cor_maior = np.array([255, 255, 255], dtype=np.uint8)


def line_intersecion(line1, line2):
        
    p1 = line1[0]
    p2 = line1[1]

    dy1 = p2[1] - p1[1]; 
    dx1 = p1[0] - p2[0]; 
    reta1 = dy1*(p1[0]) + dx1*(p1[1]);

    p3 = line2[0]
    p4 = line2[1]

    dy2 = p4[1] - p3[1]; 
    dx2 = p3[0] - p4[0]; 
    reta2 = dy2*(p3[0]) + dx2*(p3[1]);
    
    if dy1*dx2 - dy2*dx1 != 0:
        determinant = dy1*dx2 - dy2*dx1

    x = (dx2*reta1 - dx1*reta2)//determinant; 
    y = (dy1*reta2 - dy2*reta1)//determinant; 

    return (x, y)


def auto_canny(image, sigma=0.33):

    v = np.median(image)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    return edged


if __name__ == "__main__":

    cap = cv2.VideoCapture('video3.mp4')

    while(cap.isOpened()):
        ret, frame = cap.read() 
        
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)      
      
        frame_rgb = frame 
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)

    
        bordas = cv2.Canny(blur,50,150,apertureSize = 3)
        bordas_color = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
        
        lines = []
        
        lines = None
        
        mask = cv2.inRange(bordas_color, cor_menor, cor_maior) 
        
        lines = cv2.HoughLines(mask,1,np.pi/180,200)
        
        framed = None 
        
        line1 = None
        line2 = None
        
        ptos = []
        
        
        for line in lines:            
                
            for rho,theta in line:
                
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 3000*(-b))
                y1 = int(y0 + 3000*(a))
                x2 = int(x0 - 3000*(-b))
                y2 = int(y0 - 3000*(a))                

                
                if x2 != x1:
                    m = (y1-y0)/(x1-x0)
                
                h = y0 - (m * x0)      
                p1 = (x1,y1)
                p2 = (x2,y2)
                    
                
                if m < -0.4 and m > -1.4:
                    cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),1) 
                    line1 = (p1, p2)
                    
                elif m > 0.3 and m < 2.1:
                    cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),1) 
                    line2 = (p1, p2)                   
                    
                    
                if line1 is not None and line2 is not None:
                    
                    pi = line_intersecion(line1, line2)
                    ptos.append(pi) 
                
                
        #Ver média dos pontos                
        
        if len(ptos)> 0:
            
            ptos = np.array(ptos)
            
            print(ptos)
                                    
            
            if len(ptos) > 1:
                ptom = ptos.mean(axis = 0)  
                
            else:
                ptom = ptos[0]
            
            
            ptom[0] = int(ptom[0])
            ptom[1] = int(ptom[1])                   
            
                
            ptom = tuple(ptom)
                
            cv2.circle(frame, (int(ptom[0]), int(ptom[1])), 3, (255,0,0), 2) 

                          
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(bordas,'Press q to quit',(1,15), font, 0.3,(255,255,255),1,cv2.LINE_AA)
        

        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    #  When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
