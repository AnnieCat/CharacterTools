using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

//This script specifically handles the forearms
public class ForearmTwist : MonoBehaviour {
	[System.Serializable]
	public class HandInfo
	{
		public string name;
		public int blendID_90, blendID_180, blendID_270;
		public GameObject[] forearms;
		public GameObject hand;
		[HideInInspector]
		public float handRot;
		[HideInInspector]
		public float forearmRot;
		[HideInInspector]
		public enum HandDirection {left, right}
		[HideInInspector]
		public HandDirection handDirection;
	}
	
	public HandInfo[] handInfo;
	//public Text indicatorText;
	
	public SkinnedMeshRenderer body;


	void Update () {
		
		//Forearm Rotation -- "hand"les the left hand, then the right
		for(int i = 0; i<=1; i++)
		{
			//capture rotation of hand (driven by VR rig) and save it as local value handRot
			handInfo[i].handRot = handInfo[i].hand.transform.localEulerAngles.y;
			
			//Check if the hand is turning to the right or the left
			if(handInfo[i].handRot < 360 && handInfo[i].handRot > 320 )
				handInfo[i].handDirection = HandInfo.HandDirection.right;
			
			if(handInfo[i].handRot > 0 && handInfo[i].handRot < 40 )
				handInfo[i].handDirection = HandInfo.HandDirection.left;
			
			//Change the axis of the forearmRotation value, based on the direction the arm is turning
			if(handInfo[i].handDirection == HandInfo.HandDirection.left)
				handInfo[i].forearmRot = handInfo[i].hand.transform.localEulerAngles.y;
			
			else if(handInfo[i].handDirection == HandInfo.HandDirection.right)
				handInfo[i].forearmRot = -1 * (360 - handInfo[i].hand.transform.localEulerAngles.y);
			
			//rotate the forearms a percentage of the total hand rotation
			handInfo[i].forearms[0].transform.localEulerAngles = new Vector3(0, handInfo[i].forearmRot * 0.45f, 0);
			handInfo[i].forearms[1].transform.localEulerAngles = new Vector3(0, handInfo[i].forearmRot * 0.3f, 0);
			
			print("Hand "+i+" Rot: "+handInfo[i].handRot);
			
			//drive blendshapes according to rotation
			setBlendValues(i);
		}
		
		//Text for debugging
		//indicatorText.text = handInfo[1].handRot.ToString();
	}

	void setBlendValues(int handID){
		//go through all three blendshape rotation options
		for(int i = 0; i < 3; i++){
			//If we are entering the blendshape's rotation value
			if(handInfo[handID].handRot > 0+(i*90) && handInfo[handID].handRot < 90 + (i*90)){
				body.SetBlendShapeWeight((handInfo[handID].blendID_90)+(handID*3), map(handInfo[handID].handRot, i*90, 90+(i*90), 0, 100));
			}
			//If we are exiting the blendshape's rotation value
			else if(handInfo[handID].handRot > 90 + (i * 90) && handInfo[handID].handRot < 180 + (i * 90)){
				body.SetBlendShapeWeight((handInfo[handID].blendID_180)+(handID*3),map(handInfo[handID].handRot, 90 + (i*90), 180 + (i*90), 100, 0));
			}
			//if we are not within the blendshape's rotation range
			else{
				body.SetBlendShapeWeight((handInfo[handID].blendID_270)+(handID * 3), 0);
			}
		}
	}
	
	float map (float value, float aMin, float aMax, float bMin, float bMax){
		return bMin + (value - aMin ) * (bMax - bMin)/(aMax - aMin);
	}
}
