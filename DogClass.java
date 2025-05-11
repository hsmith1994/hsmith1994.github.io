// IT145
// Hunter Smith
// Professor Robinson
// Assignment 2: Write a Class

package com.Java;

public class Pet {
	
	private String petType;
	private String petName;
	private int petAge;
	private int dogSpace;
	private int catSpace;
	private int daysStay;
	private double amountDue;
	
	// default constructor
	public Pet() {
		petType = "";
		petName = "";
		petAge = 0;
		dogSpace = 0;
		catSpace = 0;
		daysStay = 0;
		amountDue = 0;
	}
	
	public void checkIn() {
		System.out.println("Pet checked in");
	}
	
	public void checkOut() {
		System.out.println("Pet checked out");
	}
	
	//getter method
	public String getPet() {
		return petType;
	}
	
	public Pet createPet() {
		System.out.println("Pet created");
	}
	
	public void updatePet() {
		System.out.println("Pet updated");
	}
	
	//getter method
	public String getPetType() {
		return petType;
	}
	
	//setter method
	public void setPetType(String petType) {
		this.petType = petType;
	}
	
	//getter method
	public String getPetName() {
		return petName;
	}
	
	//setter method
	public void setPetName(String petName) {
		this.petName = petName;
	}
	
	//getter method
	public int getPetAge() {
		return petAge;
	}
	
	//setter method
	public void setPetAge(int petAge) {
		this.petAge = petAge;
	}
	
	//getter method
	public int getDogSpace() {
		return dogSpace;
	}
	
	public void setDogSpace(int dogSpace) {
		this.dogSpace = dogSpace;
	}
	
	//getter method
	public int getCatSpace() {
		return catSpace;
	}
	
	//setter method
	public void setCatSpace(int catSpace) {
		this.catSpace = catSpace;
	}
	
	//getter method
	public int getDaysStay(int daysStay) {
		return daysStay;
	}
	
	//setter method
	public void setDaysStay(int daysStay) {
		this.daysStay = daysStay;
	}
	
	//getter method
	public double getAmountDue() {
		return amountDue;
	}
	
	//setter method
	public void setAmountDue(double amountDue) {
		this.amountDue = amountDue;
	}
}

public class Dog extends Pet {
	
	private int dogSpaceNumber;
	private double dogWeight;
	private boolean grooming;
	
	// default constructor
	public Dog() {
		dogSpaceNumber = 0;
	}
	
	//getter method
	public int getdogSpaceNumber() {
		return dogSpaceNumber;
	}
	
	//setter method
	public void setdogSpaceNumber(int dogSpaceNumber) {
		this.dogSpaceNumber = dogSpaceNumber;
	}
	
	//getter method
	public double getDogWeight() {
		return dogWeight;
	}
	
	//setter method
	public void setDogWeight(double dogWeight) {
		this.dogWeight = dogWeight;
	}
	
	//getter method
	public boolean isGrooming() {
		return grooming;
	}
	
	//setter method
	public void setGrooming(boolean grooming) {
		this.grooming = grooming;
	}
	
	//returns an object of Dog Class
	@Override
	public Dog createPet() {
		System.out.println("Dog created");
		return new Dog();
	}
	
	@Override
	public void updatePet() {
		System.out.println("Dog updated:");
		
	

	}

}
