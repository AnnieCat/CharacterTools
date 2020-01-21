using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

//drives a blendshape based on a generic rotating bone
public class GenericRotation : MonoBehaviour
{
	[System.Serializable]
	public class DriverInfo{
		
		public string blendshapeName;
		public GameObject drivingBone;
		
		[System.Serializable]
		public enum Axis {X,Y,Z};
		public Axis axis;
		
		public float lowerRotationLimit, upperRotationLimit;
		
		[HideInInspector]
		public int blendID;
		[HideInInspector]
		public float boneRot;
	}
	public DriverInfo[] driverInfo;
	private SkinnedMeshRenderer bod;
	
	
    void Start()
	{
	    bod = this.GetComponent<SkinnedMeshRenderer>();
    	Mesh m = bod.sharedMesh;
    	
		//store the ID of the blendshape which matches our "blendshape string"
		for(int i = 0; i < driverInfo.Length; i++){
			
			for(int j = 0; j < m.blendShapeCount; j++){
				if(m.GetBlendShapeName(j) == driverInfo[i].blendshapeName){
					driverInfo[i].blendID = j;
					break;
				}
			}
		}
		
    }

    void Update()
    {
	    //Capture rotation of bone and save it as local value
	    for(int i = 0; i < driverInfo.Length; i++){
	    	
	    	if(driverInfo[i].axis == GenericRotation.DriverInfo.Axis.X)
	    		driverInfo[i].boneRot = driverInfo[i].drivingBone.transform.eulerAngles.x;
	    	if(driverInfo[i].axis == GenericRotation.DriverInfo.Axis.Y)
	    		driverInfo[i].boneRot = driverInfo[i].drivingBone.transform.eulerAngles.y;
		    if(driverInfo[i].axis == GenericRotation.DriverInfo.Axis.Z)
	    		driverInfo[i].boneRot = driverInfo[i].drivingBone.transform.eulerAngles.z;
	    
		    if(driverInfo[i].boneRot > 180)
			    driverInfo[i].boneRot = driverInfo[i].boneRot - 360;
		    SetBlendValues();
	    }
    }
	
	void SetBlendValues(){
		for(int i = 0; i < driverInfo.Length; i++){
			
			float convertedNumbers = map(driverInfo[i].boneRot,driverInfo[i].lowerRotationLimit,driverInfo[i].upperRotationLimit,0,100);
			convertedNumbers = Mathf.Clamp(convertedNumbers,0,100);
			bod.SetBlendShapeWeight(driverInfo[i].blendID,convertedNumbers);
		}
	}
	
	float map(float value, float aMin, float aMax, float bMin, float bMax){
		return bMin + (value - aMin) * (bMax - bMin)/(aMax - aMin);
	}

}

