import cv2
import mediapipe as mp
import numpy as np

class FaceMeshDetector:
    FONT = cv2.FONT_HERSHEY_COMPLEX
    TEXT_COLOR = (0, 255, 255)
    BOX_COLOR = (0, 0, 255)
    THICKNESS = 1
    SCALE = 1

    def __init__(self, effects, staticMode=False, maxFaces=10, refine_landmarks=True, minDetectionCon=0.4, minTrackCon=0.5):
        self.results = None
        self.imgRGB = None
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.refine_landmarks = refine_landmarks
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces, self.refine_landmarks,
                                                 self.minDetectionCon, self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)
        self.effects = effects

    def detect_faces(self, frame: np.ndarray) -> None:
        try:
            self.imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.results = self.faceMesh.process(self.imgRGB)
            if self.results.multi_face_landmarks:
                for faceLms in self.results.multi_face_landmarks:
                    self.draw_rectangle(frame, faceLms)
                face_count = f'Faces: {len(self.results.multi_face_landmarks)}'
                effect_text = f'Effects: {self.effects}'
                cv2.putText(frame, face_count, (10, 25), self.FONT, self.SCALE, self.TEXT_COLOR, self.THICKNESS)
                cv2.putText(frame, effect_text, (10, 50), self.FONT, self.SCALE, self.TEXT_COLOR, self.THICKNESS)
                print(face_count)
        except Exception as e:
            print(f"Error in detect faces: {e}")

    def draw_rectangle(self, frame: np.ndarray, faceLms: mp.solutions.face_mesh.NamedTuple) -> None:
        try:
            ih, iw, ic = frame.shape
            x_min, x_max, y_min, y_max = iw, 0, ih, 0
            for id, lm in enumerate(faceLms.landmark):
                x, y = int(lm.x * iw), int(lm.y * ih)
                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
            if self.effects is None:
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), self.BOX_COLOR, self.THICKNESS)
            elif self.effects == 'blur':
                blur_img = cv2.blur(frame[y_min:y_max, x_min:x_max], (50, 50))
                frame[y_min:y_max, x_min:x_max] = blur_img
        except Exception as e:
            print(f"Error in draw rectangle: {e}")