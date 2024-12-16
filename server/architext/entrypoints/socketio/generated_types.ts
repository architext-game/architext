/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface LoginResponse {
  success: boolean;
  data?: LoginResponse1 | null;
  error?: string | null;
}
export interface LoginResponse1 {
  jwt_token: string;
}
export interface LoginParams {
  email: string;
  password: string;
}
export interface AuthenticateResponse {
  success: boolean;
  data?: {
    user_id: string;
  } | null;
  error?: string | null;
}
export interface AuthenticateParams {
  jwt_token: string;
}
export interface SignupResponse {
  success: boolean;
  data?: {
    user_id: string;
  } | null;
  error?: string | null;
}
export interface SignupParams {
  email: string;
  name: string;
  password: string;
}
export interface GetCurrentRoomResponse {
  success: boolean;
  data?: {
    current_room: {
      id: string;
      name: string;
      description: string;
      exits: {
        name: string;
        description: string;
      }[];
      people: {
        id: string;
        name: string;
      }[];
    } | null;
  } | null;
  error?: string | null;
}
export interface CreateConnectedRoomResponse {
  success: boolean;
  data?: {
    room_id: string;
  } | null;
  error?: string | null;
}
export interface CreateConnectedRoomParams {
  name: string;
  description: string;
  exit_to_new_room_name: string;
  exit_to_new_room_description: string;
  exit_to_old_room_name: string;
  exit_to_old_room_description: string;
}
export interface TraverseExitResponse {
  success: boolean;
  data?: {
    new_room_id: string;
  } | null;
  error?: string | null;
}
export interface TraverseExitParams {
  exit_name: string;
}
export interface OtherLeftRoomNotification {
  user_name: string;
}
export interface OtherEnteredRoomNotification {
  user_name: string;
}
