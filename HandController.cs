using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandController : MonoBehaviour
{
	private Animator myAnim;
	private float L_thumbVal, R_thumbVal, L_pointerVal, R_pointerVal;
	
    void Start()
    {
	    myAnim = this.GetComponent<Animator>();
    }

    void Update()
	{
		//thumb
		if(OVRInput.Get(OVRInput.Touch.Three)){
			L_thumbVal = Mathf.MoveTowards(L_thumbVal, 1, 7*Time.deltaTime);
			myAnim.SetFloat("L_thumb", L_thumbVal);
		}
			
		else{
			L_thumbVal = Mathf.MoveTowards(L_thumbVal, 0, 7*Time.deltaTime);
			myAnim.SetFloat("L_thumb",L_thumbVal);
		}
			
			
		if(OVRInput.Get(OVRInput.Touch.One))
		{
			R_thumbVal = Mathf.MoveTowards(R_thumbVal, 1, 7*Time.deltaTime);
			myAnim.SetFloat("R_thumb",R_thumbVal);
		}
		else
		{
			R_thumbVal = Mathf.MoveTowards(R_thumbVal,0, 7*Time.deltaTime);
			myAnim.SetFloat("R_thumb",R_thumbVal);
		}
		
		//pointer
		if(OVRInput.Get(OVRInput.Touch.PrimaryIndexTrigger))
		{
			L_pointerVal = Mathf.MoveTowards(L_pointerVal, 1, 7*Time.deltaTime);
			myAnim.SetFloat("L_pointer",L_pointerVal);
		}
		else
		{
			L_pointerVal = Mathf.MoveTowards(L_pointerVal,0,7*Time.deltaTime);
			myAnim.SetFloat("L_pointer",L_pointerVal);
		}
			
		if(OVRInput.Get(OVRInput.Touch.SecondaryIndexTrigger))
		{
			R_pointerVal = Mathf.MoveTowards(R_pointerVal, 1, 7*Time.deltaTime);
			myAnim.SetFloat("R_pointer",R_pointerVal);
		}
		else
		{	
			R_pointerVal = Mathf.MoveTowards(R_pointerVal, 0, 7*Time.deltaTime);
			myAnim.SetFloat("R_pointer",R_pointerVal);
		}

		//pinch
		myAnim.SetFloat("L_pinch", OVRInput.Get(OVRInput.Axis1D.PrimaryIndexTrigger));
		myAnim.SetFloat("R_pinch", OVRInput.Get(OVRInput.Axis1D.SecondaryIndexTrigger));

		//grip
		myAnim.SetFloat("L_grip", OVRInput.Get(OVRInput.Axis1D.PrimaryHandTrigger));
		myAnim.SetFloat("R_grip", OVRInput.Get(OVRInput.Axis1D.SecondaryHandTrigger));
	}
}
